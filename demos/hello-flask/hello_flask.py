from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1>Hello Flask</h1>"


# 多个URL对应一个视图函数
@app.route('/hi')
@app.route('/hello')
def say_hello():
    return '<h1>Hello, Flask</h1>'


# 动态路由，URL可以有默认值
@app.route('/greet/', defaults={'name': 'default name'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s</h1>' % name

# 使用<converter:variable_name>可以选择性的加上一个转换器，为变量指定规则
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post {post_id}'


import click


@app.cli.command()
def hello():
    click.echo("hello, cli")
