import os
from flask import Flask, render_template, flash, redirect, url_for
from form import loginForm, registerForm
from flask_sqlalchemy import SQLAlchemy

# todo 登录验证， 登录失败提醒， 登录成功 name传递

app = Flask(__name__)
app.secret_key = 'secret string'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',
                                                  'sqlite:////' + os.path.join(app.root_path, 'data.db'))

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(16))


# flask shell 上下文
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Users=Users)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = registerForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user_data = Users(username=username, password=password)
        db.session.add(user_data)
        db.session.commit()
        flash('Register Success, Please Login')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'admin':
            return redirect(url_for('home'))
    flash('login failed')
    return render_template('login.html', form=form)


@app.route('/home')
def home():
    form = loginForm()
    username = form.username.data
    return render_template('welcome.html', username=username)

