from flask import Flask, render_template, request, flash, url_for, redirect
from werkzeug.exceptions import abort
from hashlib import md5
import sqlite3
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adminkey'

from config import *

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/')
def index():
    conn = get_db_connection()
    conn.execute("DELETE FROM posts WHERE created < DATETIME('now', '-1 hours')").fetchall()
    posts = conn.execute('SELECT * FROM posts ORDER BY created DESC').fetchall()
    conn.close()
    return render_template("index.html", posts=posts)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        title = request.form["title"]
        # image_file = request.files['file']
        content = request.form["content"]

        # if not image_file:
        #     print("uh oh!")
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
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                            (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('upload'))

    return render_template("upload.html")