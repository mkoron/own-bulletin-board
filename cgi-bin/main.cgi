#!/usr/bin/env python3
print("Content-type: text/html\n")

import cgitb
import sqlite3
import utils 

toplevel = []
children = {}

cursor, _ = utils.connectDB()

def format(row):
    print('<p><a href="view.cgi?id={id}">{subject}</a></p>'.format(**row))
    try:
        kids = children[row['id']]
    except KeyError:
        pass
    else:
        print('<blockquote>')
        for kid in kids:
            format(kid)
        print('</blockquote>')

print("""
<html>
    <head>
        <title>A Simple Bulletin Board</title>
    </head>
    <body>
        <h1>A Simple Bulletin Board</h1>
    """)

cursor.execute("SELECT * FROM messages")
rows = cursor.fetchall()

for row in rows:
    parent_id = row['reply_to']
    if parent_id is None:
        toplevel.append(row)
    else:
        children.setdefault(parent_id, []).append(row)

print('<p>')

for row in toplevel:
    format(row)

print("""
      </p>
      <hr>
      <a href='edit.cgi'>Post a message</a>
   </body>
</html>
"""
)
