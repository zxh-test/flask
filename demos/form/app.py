from flask import render_template, Flask, flash, redirect, url_for, request
from form import LoginForm

app = Flask(__name__)

app.secret_key = 'secret string'


@app.route('/')
def index():
    return 'Welcome {}'


@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome %s' % username)
        return redirect(url_for('basic'))
    return render_template('basic.html', form=form)
