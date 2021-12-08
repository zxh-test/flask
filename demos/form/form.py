from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(message='please input username')],
                           render_kw={'placeholder': 'your name'})
    password = PasswordField(label='Password', validators=[Length(6, 16, message='Password length is wrong')],
                             render_kw={'placeholder': 'your password'})
    remember = BooleanField(label='Remember')
    submit = SubmitField(label='Submit')


# 行内验证器
class FortyTwoForm(FlaskForm):
    answer = IntegerField('input number')
    submit = SubmitField()

    def validate_answer(forty, field):
        if field.data != 42:
            raise ValueError('Must be 42')
