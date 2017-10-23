#!/usr/bin/env python3
print("Content-type: text/html\n")

import cgitb
import sqlite3
import cgi, sys, os

#Remove before production deployment
cgitb.enable()

BASE_DIR = os.path.dirname(os.path.abspath(__file__ + "/../"))
db_path = os.path.join(BASE_DIR, 'bulletin_board.sqlite')

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

form = cgi.FieldStorage()
id = form.getvalue('id')

print("""
<html>
    <head>
        <title>View Message</title>
    </head>
    <body>
        <h1>View Message</h1>
    """)

try:
    id = int(id)
except:
    print('Invalid message ID')
    sys.exit()

c.execute('SELECT * FROM messages WHERE id = {}'.format(id))
rows = c.fetchall()

if not rows:
    print('Unknown message ID')
    sys.exit()

row = rows[0]

print("""
    <p><b>Subject:</b> {subject}<br>
    <b>Sender:</b> {sender}<br>
    <pre>{text}</pre>
    </p>
    <hr>
    <a href='main.cgi'>Back to the main page</a>
    <a href='edit.cgi?reply_to={id}'>Reply</a>
</body>
</html>
""".format(**row))