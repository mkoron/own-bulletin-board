#!/usr/bin/env python3
print("Content-type: text/html\n")

import cgitb
import sqlite3
import os.path

#Remove before production deployment
cgitb.enable()

BASE_DIR = os.path.dirname(os.path.abspath(__file__ + "/../"))
db_path = os.path.join(BASE_DIR, 'bulletin_board.sqlite')

toplevel = []
children = {}

# Row factory
# It accepts the cursor and the original row as a tuple and will return the real result row.
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn = sqlite3.connect(db_path)
conn.row_factory = dict_factory
c = conn.cursor()

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

c.execute("SELECT * FROM messages")
rows = c.fetchall()

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
