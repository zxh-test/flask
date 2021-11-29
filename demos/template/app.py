from flask import Flask, render_template, flash, url_for, redirect

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
app.secret_key = 'secret string'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)


@app.route('/watchlist2')
def watchlist2():
    return render_template('watchlist_with_static.html', user=user, movies=movies)


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


@app.template_filter('filter_len')
def my_length(s):
    return len(s)


# 注册自定义测试器
@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False


# 模版辅助工具
@app.route('/test/')
def test_fun():
    return render_template('test.html')


# 使用flash() 函数"闪现"消息
@app.route('/flash')
def just_flash():
    flash('I am flash who is looking for me?')
    return redirect(url_for('index'))


# 404错误处理器
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404
