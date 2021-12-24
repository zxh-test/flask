from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import Email


class SubscribeForm(FlaskForm):
    mail = StringField('mail', validators=[Email(message='格式错误')])
    subscribe = SubmitField()