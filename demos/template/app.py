from flask import Flask, render_template

user = {
    "username": "Bob",
    "bio": "a boy like movies and music"}


movies = [
    {"name": "钢铁侠", "years": "2005"},
    {"name": "复仇者联盟", "years": "2006"},
    {"name": "绿巨人", "years": "2007"},
    {"name": "西红柿首富", "years": "2010"},
    {"name": "夏洛特烦恼", "years": "2005"},
    {"name": "钢铁侠2", "years": "2005"}
]

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1>Home</h1>"


@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)
