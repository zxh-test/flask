from flask import render_template, Flask, flash, redirect, url_for, request
from form import LoginForm, FortyTwoForm, uploadFile

app = Flask(__name__)

app.secret_key = 'secret string'


@app.route('/')
def index():
    return 'Welcome'


@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome %s' % username)
        return redirect(url_for('basic'))
    return render_template('basic.html', form=form)


@app.route('/number', methods=['GET', 'POST'])
def validate_number():
    forty = FortyTwoForm()
    if forty.validate_on_submit():
        return 'welcome'
    return render_template('number.html', forty=forty)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    upload = uploadFile()
    return render_template('upload.html', upload=upload)
