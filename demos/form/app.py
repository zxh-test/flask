from flask import render_template, Flask,request
from form import LoginForm

app = Flask(__name__)

app.secret_key = 'secret string'


@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    if form.validate_on_submit():
        return 'welcome {}'.format(request.form.get('username'))
    return render_template('basic.html', form=form)