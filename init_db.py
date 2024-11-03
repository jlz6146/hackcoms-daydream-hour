import sqlite3
import time
from hashlib import md5
import os
from config import *
from werkzeug.utils import secure_filename
import base64

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

filename = secure_filename("image.png")

data = ""
with open(filename, 'rb') as f:
    data = base64.b64encode(f.read()).decode('utf-8')

cur.execute("INSERT INTO users (user_alias, email) VALUES (?, ?)",
            ('minmendo', 'superboy@mushroomkingdom.wahh')
            )

cur.execute("INSERT INTO posts (title, file_name, img, content, extension, user) VALUES (?, ?, ?, ?, ?, ?)",
            ('First Post', filename, data, 'Content for the first post', 'png', 1)
            )

cur.execute("INSERT INTO comments (user_alias, content, associated_post) VALUES (?, ?, ?)",
            ('obiwan', 'hello there', 1)
            )

cur.execute("INSERT INTO posts (title, file_name, img, content, extension, user) VALUES (?, ?, ?, ?, ?, ?)",
            ('Second Post', filename, data, 'Content for the second post', 'png', 1)
            )


connection.commit()
connection.close()
