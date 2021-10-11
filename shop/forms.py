from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField,TextAreaField
from wtforms.validators import DataRequired , Email , EqualTo,ValidationError
from flask_wtf.file import FileAllowed,FileField
import email_validator
from shop.models  import *


class RegistretionForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired('это поле обязателно'),Email('не правильный email ') ])
    password = PasswordField('password',validators=[DataRequired('это поле обязателно')])
    confirm_password = PasswordField('confirm password',validators=[DataRequired('это поле обязателно'),EqualTo('password')])
    submit = SubmitField('submit')


    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user :
            raise ValidationError('такой email уже существует')

class PostForm(FlaskForm):
    title = StringField('title',validators=[DataRequired('это поле обязательно для заполнения')])
    content = TextAreaField('content',validators=[DataRequired('это поле обязательно для заполнения')])
    image = FileField('image',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('submit')