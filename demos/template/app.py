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


# 注册模版上下文处理函数
@app.context_processor
def inject_foo():
    foo = 'I am foo.'
    return dict(foo=foo)


# 注册模版全局函数
@app.template_global()
def bar():
    return 'I am bar'


from flask import Markup


# 注册自定义过滤器
@app.template_filter()
def musical(s):
    return s + Markup(' &#9835;')


# 注册自定义测试器
@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False


@app.route('/test/')
def test_fun():
    return render_template('test.html')