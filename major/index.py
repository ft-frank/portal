from flask import Flask, render_template, redirect, url_for, flash, abort, send_from_directory
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm, CSRFProtect
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectField
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
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable = True)
    role = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    school = db.Column(db.String(100))
    grade = db.Column(db.String(20))
    class_ = db.relationship('Class', backref='users')

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class HomeworkSol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    file_path = db.Column(db.String(200))
    class_ = db.relationship('Class', backref='homework_solutions')


class QuestionBank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    file_path = db.Column(db.String(200))
    class_ = db.relationship('Class', backref='question_banks')

class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(min=5, max=50)], render_kw={"placeholder": "Email", "type": "email"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    class_id = SelectField("Class", coerce=int)
    first_name = StringField(validators=[InputRequired(), Length(min=0, max=50)])
    last_name = StringField(validators=[Length(min=0, max=50)])
    school = StringField(validators=[Length(min=0, max=50)])
    grade = SelectField(
        choices=[('12'), ('11'), ('None')],
        validators=[InputRequired()],
        render_kw={"placeholder": "Grade"})
    role = SelectField(
        choices=[('student', 'Student'), ('tutor', 'Tutor'), ('admin', 'Admin')],
        validators=[InputRequired()],
        render_kw={"placeholder": "Role"}
    )
    submit = SubmitField("Register")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("That email is already in use.")

class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=5, max=50)])
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField("Login")

class HomeworkForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    class_id = SelectField("Class", coerce=int)
    file = FileField('Upload File', validators=[FileAllowed(['pdf', 'docx', 'png', 'jpg']), InputRequired()])
    class_id = SelectField("Class", coerce=int, validators=[InputRequired()])
    submit = SubmitField('Create')

@app.route('/')
@login_required
def home():
    return render_template('home.html', title='Home', current_page = 'home', user=current_user)

@app.route('/invoices')
@login_required
def invoices():
    return render_template('invoices.html', title = 'Invoices', current_page = 'invoices')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin.index'))  
            elif user.role == 'student':
                return redirect(url_for('home'))  
            else:
                return redirect(url_for('home')) 
        flash("Incorrect email or password.", "danger")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    form.class_id.choices = [(c.id, c.name) for c in Class.query.all()]
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(email=form.email.data, password=hashed_password, class_id = form.class_id.data, first_name = form.first_name.data, last_name = form.first_name.data, school = form.school.data, grade = form.grade.data, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully!", "success")
    else:
        flash("An existing account exists with this email.", "danger")     
    return render_template('register.html', form=form)

@app.route('/hw_solutions')
@login_required
def hw_solutions():
    homeworks = HomeworkSol.query.filter_by(class_id = current_user.class_id)
    return render_template('homework.html', homeworks=homeworks, user = current_user, current_page = 'hw_solutions')

@app.route('/hw_solutions/<filename>')
@login_required
def show_homework_sol(filename):
    if not filename.endswith('.pdf'):
        abort(403)
    folder = os.path.join(app.root_path, app.config['HOMEWORK_SOL_FOLDER'])
    return send_from_directory(folder, filename)

@app.route('/upload_homework_sol', methods=['GET', 'POST'])
@role_required('admin', 'tutor')
def create_homework():
    form = HomeworkForm()
    form.class_id.choices = [(c.id, c.name) for c in Class.query.all()]
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename.replace(" ", "_").replace("%", "_"))
        path = os.path.join(app.root_path, app.config['HOMEWORK_SOL_FOLDER'], filename)
        form.file.data.save(path)
        db.session.add(HomeworkSol(title=form.title.data, filename=filename, class_id=form.class_id.data, file_path=path))
        db.session.commit()
        flash("Homework uploaded successfully!", "success")
    return render_template('create_homework.html', form=form)

@app.route('/questions')
@login_required
def questions():
    questions = QuestionBank.query.filter_by(class_id = current_user.class_id)
    return render_template('questions.html', questions=questions, current_page = 'questions', user = current_user)

@app.route('/questions/<filename>')
@login_required
def show_questions(filename):
    if not filename.endswith('.pdf'):
        abort(403)
    folder = os.path.join(app.root_path, app.config['QUESTIONS_FOLDER'])
    return send_from_directory(folder, filename)

@app.route('/upload_questions', methods=['GET', 'POST'])
@role_required('admin', 'tutor')
def upload_questions():
    form = HomeworkForm()
    form.class_id.choices = [(c.id, c.name) for c in Class.query.all()]
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename.replace(" ", "_").replace("%", "_"))
        path = os.path.join(app.root_path, app.config['QUESTIONS_FOLDER'], filename)
        form.file.data.save(path)
        db.session.add(QuestionBank(title=form.title.data, filename=filename, class_id=form.class_id.data, file_path=path))
        db.session.commit()
        flash("Question uploaded successfully!", "success")
    return render_template('create_questions.html', form=form)

# Admin setup
class AdminModelView(ModelView):
    None
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

admin = Admin(app, name='Admin Panel')
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Class, db.session))
admin.add_view(AdminModelView(HomeworkSol, db.session))
admin.add_view(AdminModelView(QuestionBank, db.session))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
