import os
from threading import Thread
from flask import Flask, render_template, redirect, url_for, jsonify
from flask_mail import Mail, Message
from form import SubscribeForm
from sendgrid.helpers.mail import Mail as SGMail, Email as SGEmail, Content, To
from sendgrid import SendGridAPIClient

app = Flask(__name__)
mail = Mail(app)

app.config.update(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('SENDGRID_API_KEY'),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_DEFAULT_SENDER=('zxh', os.getenv('MAIL_USERNAME')),
    SECRET_KEY=os.getenv('SECRET_KEY', 'secret string')

)


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_smtp_mail(subject, to, body):
    message = Message(subject=subject, recipients=[to], body=body)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


def send_api_mail(subject, to, body):
    sg = SendGridAPIClient(api_key='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')
    from_email = SGEmail('dhaoren23@gmail.com')
    to_email = To(to)
    content = Content('text/plain', body)
    email = SGMail(from_email, to_email, subject, content)
    sg.client.mail.send.post(request_body=email.get())


@app.route('/subscribe', methods=['POST', 'GET'])
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        mail_address = form.mail.data
        # send_smtp_mail('subscribe success', mail_address, 'subscribe success')
        send_api_mail('api subscribe', mail_address, 'success')
        return redirect(url_for('index'))
    return render_template('subscribe.html', form=form)


@app.route('/')
def index():
    return jsonify({'result': 'success'})
