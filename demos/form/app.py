import uuid, os
from flask import render_template, Flask, flash, redirect, url_for, session, send_from_directory
from form import LoginForm, FortyTwoForm, UploadFile, RichTextForm
from flask_ckeditor import CKEditor

app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['CKEDITOR_SEERVE_LOCAL'] = True

app.secret_key = 'secret string'
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'upload_images')


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


# 重新为file命名
def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    upload = UploadFile()
    if upload.validate_on_submit():
        f = upload.photo.data  # f的值：<FileStorage: 'test_pic1614858602921-2.png' ('image/png')>
        filename = random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('upload success')
        session['filenames'] = [filename]
        return redirect(url_for('show_images'))
    return render_template('upload.html', upload=upload)


@app.route('/uploaded-images')
def show_images():
    return render_template('show_image.html')


@app.route('/upload/<path:filename>')
def get_file(filename):
    print(filename)
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/ckeditor', methods=['GET', 'POST'])
def ckeditor():
    form = RichTextForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        return render_template('post.html', title=title, body=body)
    return render_template('ckeditor.html', form=form)
