from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, ValidationError


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(message='please input username')],
                           render_kw={'placeholder': 'your name'})
    password = PasswordField(label='Password', validators=[Length(6, 16, message='Password length is wrong')],
                             render_kw={'placeholder': 'your password'})
    remember = BooleanField(label='Remember')
    submit = SubmitField(label='Submit')


# 工厂函数形式的全局验证器
def is_43(message=None):
    def _is_43(form, field):
        if field.data != 43:
            raise ValidationError(message)
    return _is_43


# 定义行内验证器
class FortyTwoForm(FlaskForm):
    answer = IntegerField('input number', validators=[is_43(message='must 43')])
    submit = SubmitField()

    def validate_answer(form, field):
        if field.data != 42:
            raise ValidationError('Must be 42')


# 定义文件上传表单
class uploadFile(FlaskForm):
    photo = FileField()
    submit = SubmitField()