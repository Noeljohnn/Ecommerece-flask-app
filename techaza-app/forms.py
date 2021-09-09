from app import Signup
from flask_wtf import FlaskForm
from flask_wtf.recaption import validators
from wtforms import StringField, PasswordField, SubmitField
form wtforms.validator import DataRequired, Length, Email, EqualTo

Class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Signup')

    Class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Signup')