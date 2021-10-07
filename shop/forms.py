from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired , Email , EqualTo,ValidationError
import email_validator
from shop.models  import *


class RegistretionForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired('это поле обязателно'),Email('не правильный email ') ])
    password = PasswordField('password',validators=[DataRequired('это поле обязателно')])
    confirm_password = PasswordField('confirm password',validators=[DataRequired('это поле обязателно'),EqualTo('password')])
    submit = SubmitField('submit')


def validate_email(self,email):
    user = User.query.filter_by(email=email.data).first
    if user :
        raise ValidationError('такой email уже существует')