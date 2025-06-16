from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    homework = db.relationship('Homework', backref='class_')


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


class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    submissions = db.relationship('HomeworkSubmission', backref='homework')


class HomeworkSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_detail.id'))
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id'))
    file_path = db.Column(db.String(200))  # path to uploaded file
    submitted_on = db.Column(db.DateTime)


class QuestionBank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Text)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))


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

# Pages


@app.route('/')
@login_required
def home():
    return render_template('home.html', title = 'Home', current_page = 'home')

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
    return render_template('homework.html', title='Homework', current_page = 'homework')

@app.route('/hw_solutions')
@login_required
def hw_solutions():
    return render_template('solutions.html', title='HomeworkSolutions', current_page = 'hw_solutions')

@app.route('/questions')
@login_required
def questions():
    return render_template('questions.html', title='Questions', current_page = 'questions')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html', title='Settings', current_page = 'settings')





# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server
    with app.app_context():
        db.create_all()  # 🔥 This creates the tables based on your models
    app.run(debug=True)