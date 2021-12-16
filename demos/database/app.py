import os
import sys
from flask import Flask, flash, redirect, render_template, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

# todo: 使用backref简化双向关系定义

# 判断系统，系统不同database uri不同
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))
app.secret_key = 'secret_string'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# 创建python shell 上下文
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Note=Note, Post=Post, Comment=Comment)


# 定义 Note数据模型
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)


# add note form
class AddNote(FlaskForm):
    body = TextAreaField('Body', validators=[DataRequired()])
    save = SubmitField('Save')


# edit note form
class EditNote(FlaskForm):
    body = TextAreaField('Body', validators=[DataRequired()])
    edit = SubmitField('Edit')


# delete note form
class DeleteNoteForm(FlaskForm):
    delete = SubmitField('Delete')


@app.route('/')
def index():
    form = DeleteNoteForm()
    notes = Note.query.all()
    return render_template('index.html', notes=notes, form=form)


# add note
@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    form = AddNote()
    if form.validate_on_submit():
        body = form.body.data
        note = Note(body=body)
        db.session.add(note)
        db.session.commit()
        flash('Your note is save.')
        return redirect(url_for('index'))
    return render_template('note.html', form=form)


# edit note
@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    form = EditNote()
    note = Note.query.get(note_id)
    if form.validate_on_submit():
        note.body = form.body.data
        db.session.commit()
        flash('Your note is edit.')
        return redirect(url_for('index'))
    form.body.data = note.body
    return render_template('edit_note.html', form=form)


# delete note
@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    form = DeleteNoteForm()
    if form.validate_on_submit():
        note = Note.query.get(note_id)
        db.session.delete(note)
        db.session.commit()
        flash('Your note is delete.')
    else:
        abort(400)
    return redirect(url_for('index'))


"""
创建作者对应作品的模型，基于一对多的单向关系
"""


# Author
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    phone = db.Column(db.String(20))
    articles = db.relationship('Article')


# Article
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))


"""
创建作家和书的模型，基于一对多的双向关系
"""


# Writer
class Writer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    books = db.relationship('Book', back_populates='writers')


# Book
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    writer_id = db.Column(db.Integer, db.ForeignKey('writer.id'))
    writers = db.relationship('Writer', back_populates='books')


# 级联操作
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    body = db.Column(db.Text)
    comments = db.relationship('Comment', back_populates='posts', cascade='all')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    posts = db.relationship('Post', back_populates='comments')


# 事件监听
class Draft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    edit_time = db.Column(db.Integer, default=0)


# set事件监听处理函数
@db.event.listens_for(Draft.body, 'set')
def add_edit_time(target, value, oldvalue, initiator):
    if target.edit_time is not None:
        target.edit_time += 1