from flask import Flask, flash, redirect, render_template, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:////' + os.path.join(app.root_path, 'data.db'))
app.secret_key = 'secret_string'
db = SQLAlchemy(app)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Note=Note)


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
