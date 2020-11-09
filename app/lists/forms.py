from flask_wtf import FlaskForm
from wtforms import (BooleanField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length, NumberRange, Optional, ValidationError)
from app.models import User, Family, List, Item

# Form for registration displayed on register.html.
class AddItem(FlaskForm):    
    value = StringField('Item Name', validators=[DataRequired(), Length(min=4, max=25, message="Must be between 4 and 25 characters")])
    submit = SubmitField('Add')