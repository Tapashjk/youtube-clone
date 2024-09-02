from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Define forms
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional(), Length(min=10, max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    profile_picture = FileField('Profile Picture', validators=[Optional()])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=200)])
    terms = BooleanField('I agree to the terms and conditions', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    forgot_password = SubmitField('Forgot Password?')
    submit = SubmitField('Login')

# Dummy user store
users = {}

@app.route('/')
def home():
    return render_template('templates/login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = users.get(email)
        if user and check_password_hash(user['password'], password):
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your email and/or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        phone = form.phone.data
        password = generate_password_hash(form.password.data)
        profile_picture = form.profile_picture.data
        bio = form.bio.data
        terms = form.terms.data
        
        if email in users:
            flash('Email already registered', 'danger')
        elif not terms:
            flash('You must agree to the terms and conditions', 'danger')
        else:
            users[email] = {
                'username': username,
                'phone': phone,
                'password': password,
                'profile_picture': profile_picture,
                'bio': bio
            }
            flash('Registration successful! You can now log in', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
