from flask import Flask, render_template, request, flash, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from hashlib import md5
import sqlite3
import time
import os
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adminkey'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'pics')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

from config import *

class CommentForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    body = StringField("Comment Content", validators=[DataRequired()])
    submit = SubmitField("Post")

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(conn, post_id):
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    if post is None:
        abort(404)
    return post

def get_comments(conn, post_id):
    comments = conn.execute(f'SELECT * FROM comments WHERE associated_post={post_id} ORDER BY created DESC').fetchall()
    return comments

def clear_db(conn):
    conn.execute("DELETE FROM comments WHERE created < DATETIME('now', '-1 hours')")
    conn.execute("DELETE FROM posts WHERE created < DATETIME('now', '-1 hours')")

@app.route('/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    conn = get_db_connection()
    post = get_post(conn, post_id)
    comments = get_comments(conn, post_id)
    if request.method == 'POST':
        user = request.form["user_alias"]
        comment = request.form["content"]
        if not user or not comment:
            flash('Need name or comment content')
        else:
            clear_db(conn)
            conn.execute('INSERT INTO comments (user_alias, content, associated_post) VALUES (?, ?, ?)', (user, comment, post_id))
            conn.commit()
            comments = get_comments(conn, post_id)
            conn.close()
            url_str = '/' + str(post_id)
            return render_template('post.html', post=post, comments=comments)
    conn.close()
    return render_template('post.html', post=post, comments=comments)

@app.route('/')
def index():
    conn = get_db_connection()
    clear_db(conn)
    posts = conn.execute('SELECT * FROM posts ORDER BY created DESC').fetchall()
    conn.close()
    return render_template("index.html", posts=posts)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/login')
def login():
    return render_template("login.html")

def convert_to_binary(filename):
    with open(filename, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
        return data
    return None

def write_to_file(data, filename):
    write_to = os.path.join(UPLOAD_DIR, filename)
    with open(write_to, 'w') as f:
        f.write(data.decode('utf-8'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        title = request.form["title"]
        image_file = request.form['pic']
        content = request.form["content"]
        if not image_file:
            flash("No upload.")
        open(image_file, 'r')
        filename = secure_filename(image_file)
        data = convert_to_binary(filename)
        # write_to_file(filename, data)
        if not data:
            flash("No upload.")
        extension = image_file.rsplit('.', 1)[1].lower()
        if extension not in ALLOWED_EXTENSIONS:
            flash("Not an image.")
        # else:
        #     extension = image_file.filename.rsplit('.', 1)[1].lower()
        #     if extension not in ALLOWED_EXTENSIONS:
        #         print("try again!")
        #     else:
        #         filename = md5(image_file.read() +
        #                    str(round(time.time() * 1000))
        #                   ).hexdigest() + '.' + extension
        #         image_file.seek(0)
        #         image_file.save(os.path.join(UPLOAD_DIR, filename))
        if not content:
            flash("Please ensure your post has content! ")
        else:
            conn = get_db_connection()
            clear_db(conn)
            conn.execute('INSERT INTO posts (title, file_name, img, content, extension) VALUES (?, ?, ?, ?, ?)',
                            (title, filename, data, content, extension))
            conn.commit()
            conn.close()
            return redirect(url_for('upload'))

    return render_template("upload.html")