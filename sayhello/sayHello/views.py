from flask import render_template, flash, redirect, url_for
from sayhello.sayHello import app, db
from forms import HelloForm
from models import Message


@app.route('/', methods=['GET', 'POST'])
def index():
    form = HelloForm()
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Message(name=name, body=body)
        db.session.add(message)
        db.session.commit()
        flash('Your message have been sent to the world')
        return redirect(url_for('index'))
    return render_template('index.html', form=form, messages=messages)