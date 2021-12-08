from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(message='please input username')],
                           render_kw={'placeholder': 'your name'})
    password = PasswordField(label='Password', validators=[Length(6, 16, message='Password length is wrong')],
                             render_kw={'placeholder': 'your password'})
    remember = BooleanField(label='Remember')
    submit = SubmitField(label='Submit')
