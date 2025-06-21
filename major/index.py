from flask import Flask, render_template, redirect, url_for, flash, Response, abort, send_from_directory, send_file
from functools import wraps
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm, CSRFProtect
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.utils import secure_filename
import os
import mimetypes





app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['HOMEWORK_SOL_FOLDER'] = 'static/homework_sol'
app.config['QUESTIONS_FOLDER'] = 'static/questions'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)





login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


#RBAC
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if current_user.role not in roles:
                abort(403)  # Forbidden
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

# Databases


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'tutor', 'student'
    student_details = db.relationship('StudentDetail', backref='user', uselist=False)


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    students = db.relationship('StudentDetail', backref='class_')
    questions = db.relationship('QuestionBank', backref='class_')
    homework = db.relationship('HomeworkSol', backref='class_')


class StudentDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    school = db.Column(db.String(100))
    grade = db.Column(db.String(20))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    invoices = db.relationship('Invoice', backref='student')
    submissions = db.relationship('HomeworkSubmission', backref='student')


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_detail.id'))
    amount = db.Column(db.Float, nullable=False)
    is_paid = db.Column(db.Boolean, default=False)


class HomeworkSol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    file_path = db.Column(db.String(200))  # Path to locally stored file
    submissions = db.relationship('HomeworkSubmission', backref='homework')



class HomeworkSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_detail.id'))
    homework_id = db.Column(db.Integer, db.ForeignKey('homework_sol.id'))
    file_path = db.Column(db.String(200))  # path to uploaded file
    submitted_on = db.Column(db.DateTime)


class QuestionBank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    file_path = db.Column(db.String(200))  # Path to locally stored file



# Forms
class RegisterForm(FlaskForm):
    email = StringField(
        validators=[
            InputRequired(),
            Email(message='Invalid email address'),
            Length(min=5, max=50)
        ],
        render_kw={"placeholder": "Email", "type": "email"}
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Password"}
    )

    role = SelectField(
        choices=[('student', 'Student'), ('tutor', 'Tutor'), ('admin', 'Admin')],
        validators=[InputRequired()],
        render_kw={"placeholder": "Role"}
    )

    submit = SubmitField("Register")

    def validate_email(self, email):
        existing_user = User.query.filter_by(email=email.data).first()
        if existing_user:
            raise ValidationError("That email is already in use. Please use a different one.")

class LoginForm(FlaskForm):
    email = StringField(
        validators=[InputRequired(), Length(min=5, max=50)],
        render_kw={"placeholder": "Email"}
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Password"}
    )

    submit = SubmitField("Login")

class HomeworkForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    file = FileField('Upload File', validators=[FileAllowed(['pdf', 'docx', 'png', 'jpg'], 'Only documents and images allowed'), InputRequired()])
    class_id = SelectField("Class", coerce=int, validators=[InputRequired()])
    submit = SubmitField('Create')



# Pages


@app.route('/')
@login_required
def home():
    return render_template('home.html', title = 'Home', current_page = 'home', user = current_user)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
    return render_template('login.html', title = 'Login', current_page = 'login', form = form)

@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, password = hashed_password, role = form.role.data)
        db.session.add(new_user)
        db.session.commit() 
        flash("New Account created succesfully!", "success")
        flash(f"Their email: {form.email.data}, Their password: {form.password.data}, Their role: {form.role.data}")

    else:
        flash("An existing account exists with this email.", "danger")
    return render_template('register.html', title = 'Register', current_page = 'register', form = form)

@app.route('/invoices')
@login_required
def invoices():
    return render_template('invoices.html', title = 'Invoices', current_page = 'invoices')

@app.route('/homework')
@login_required
def homework():
    homeworks = HomeworkSol.query.all()  # 👈 Get all homework
    return render_template('homework.html', title='Homework', current_page='homework', homeworks=homeworks)

@app.route('/questions')
@login_required
def questions():
    return render_template('questions.html', title='Questions', current_page = 'questions')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html', title='Settings', current_page = 'settings')

@app.route('/upload_questions', methods=['GET', 'POST'])
@role_required('admin', 'tutor')
def upload_questions():
    form = HomeworkForm()
    form.class_id.choices = [(c.id, c.name) for c in Class.query.all()]

    if form.validate_on_submit():
        
        file = form.file.data
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['QUESTIONS_FOLDER'], secure_filename(file.filename))
        file.save(path)
        questions = QuestionBank(
            title = form.title.data,
            filename = file.filename,
            class_id = form.class_id.data,
            file_path = path)
        db.session.add(questions)
        db.session.commit()
        flash("Question uploaded to question bannk succesfully!", "success")
        return render_template('create_questions.html', form = form, title = 'Create Questions')


    return render_template('create_questions.html', form=form, title='Create Questions')

@app.route('/questions/<filename>/')
@login_required
def show_questions(filename):
    if not filename.endswith('.pdf'):
        abort(403)  # Only allow PDFs

    folder = os.path.join(app.root_path, 'static', 'questions')
    return send_from_directory(folder, filename, as_attachment=False, mimetype=mimetypes.guess_type(filename)[0])

@app.route('/hw_solutions')
@login_required
def hw_solutions():
    homeworks = HomeworkSol.query.all()  # 👈 Get all homework
    return render_template('solutions.html', title='HomeworkSolutions', current_page = 'hw_solutions', homeworks = homeworks)

@app.route('/upload_homework_sol', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'tutor')
def create_homework():
    form = HomeworkForm()
    form.class_id.choices = [(c.id, c.name) for c in Class.query.all()]
    if form.validate_on_submit():
        
        file = form.file.data
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['HOMEWORK_SOL_FOLDER'], secure_filename(file.filename))
        file.save(path) #Saves File to Database
        homework = HomeworkSol(
            title = form.title.data,
            filename = file.filename,
            class_id = form.class_id.data,
            file_path = path)
        db.session.add(homework)
        db.session.commit() 
        flash("Homework Solutions uploaded succesfully!", "success")
    return render_template('create_homework.html', form = form)

@app.route('/hw_solutions/<filename>/')
@login_required
def show_homework_sol(filename):
    if not filename.endswith('.pdf'):
        abort(403)  # Only allow PDFs

    folder = os.path.join(app.root_path, 'static', 'homework_sol')
    return send_from_directory(folder, filename, as_attachment=False, mimetype=mimetypes.guess_type(filename)[0])





#Admin View
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
    
class HomeworkModelView(AdminModelView):
    form_columns = ['title', 'filename', 'class_id', 'file_path']
    form_args = {
        'class_id': {
            'label': 'Class',
            'query_factory': lambda: Class.query.all(),
            'allow_blank': False
        }
    }

admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(StudentDetail, db.session))
admin.add_view(AdminModelView(Invoice, db.session))
admin.add_view(AdminModelView(Class, db.session))
admin.add_view(AdminModelView(HomeworkSol, db.session))
admin.add_view(AdminModelView(HomeworkSubmission, db.session))
admin.add_view(AdminModelView(QuestionBank, db.session))




# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server
    with app.app_context():
        db.create_all()  # 🔥 This creates the tables based on your models
    app.run(debug=True)