from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField(label='User name', validators=[DataRequired()], render_kw={'placeholder': 'your name'})
    password = PasswordField(label='Password', validators=[Length(6, 16, message='密码格式错误')],
                             render_kw={'placeholder': 'your password'})
    remember = BooleanField(label='Remember')
    submit = SubmitField(label='Submit')
