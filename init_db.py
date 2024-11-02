import sqlite3
import time
from hashlib import md5
import os
from config import *

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

filename = "image.png"


cur.execute("INSERT INTO posts (title, filename, content) VALUES (?, ?, ?)",
            ('First Post', filename, 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, filename, content) VALUES (?, ?, ?)",
            ('Second Post', filename, 'Content for the second post')
            )

connection.commit()
connection.close()
