#!/usr/bin/env python3
print("Content-type: text/html\n")

import cgitb
import sqlite3
import cgi, sys, os

#Remove before production deployment
cgitb.enable()

BASE_DIR = os.path.dirname(os.path.abspath(__file__ + "/../"))
db_path = os.path.join(BASE_DIR, 'bulletin_board.sqlite')

def quote(string):
    if string:
        return string.replace("'", "\\")
    else:
        return string

conn = sqlite3.connect(db_path)
c = conn.cursor()

form = cgi.FieldStorage()

sender = quote(form.getvalue('sender'))
subject =quote(form.getvalue('subject'))
text = quote(form.getvalue('text'))
reply_to = quote(form.getvalue('reply_to'))

if not (sender and subject and text):
    print('Please fill all the fields')
    sys.exit()

if reply_to is not None:
    query = "INSERT INTO messages(reply_to, sender, subject, text) VALUES ('{}', '{}', '{}', '{}')".format(int(reply_to), sender, subject, text)
else:
    query = "INSERT INTO messages(sender, subject, text) VALUES ('{}', '{}', '{}')""".format(sender, subject, text)

c.execute(query)
conn.commit()

print("""
<html>
    <head>
        <title>Message Saved</title>
    </head>
    <body>
        <h1>The Message has been saved</h1>
        <hr>
        <a href='main.cgi'>Back to the main page</a>
    </body>
</html>
""")