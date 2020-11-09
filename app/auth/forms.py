from flask_wtf import FlaskForm
from wtforms import (BooleanField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length, NumberRange, Optional, ValidationError)
from app.models import User, Family

# Form for registration displayed on register.html.
class RegisterForm(FlaskForm):    
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25, message="Must be between 4 and 25 characters")])
    fullname = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=35, message="Must be between 6 and 35 characters")])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])
    existing_family = BooleanField('Family already exists')
    family_name = StringField('Family Name', validators=[DataRequired()])
    family_password = PasswordField('Family Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            self.username.errors.append('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            self.email.errors.append('Please use a different email address.')    

    """def validate_family_name(self, family_name):
        family = Family.query.filter_by(name=family_name.data).first()
        if family is not None:
            self.family_name.errors.append('Please use a different family name.')"""
    

# Form for logging in displayed on login.html.
class LoginForm(FlaskForm):    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')