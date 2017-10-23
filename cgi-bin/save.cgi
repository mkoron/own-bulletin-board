#!/usr/bin/env python3
print("Content-type: text/html\n")

import utils
import cgi, sys

cursor, conn = utils.connectDB(False)

form = cgi.FieldStorage()

sender = utils.quote(form.getvalue('sender'))
subject =utils.quote(form.getvalue('subject'))
text = utils.quote(form.getvalue('text'))
reply_to = utils.quote(form.getvalue('reply_to'))

if not (sender and subject and text):
    print('Please fill all the fields')
    sys.exit()

if reply_to is not None:
    query = "INSERT INTO messages(reply_to, sender, subject, text) VALUES ('{}', '{}', '{}', '{}')".format(int(reply_to), sender, subject, text)
else:
    query = "INSERT INTO messages(sender, subject, text) VALUES ('{}', '{}', '{}')""".format(sender, subject, text)

cursor.execute(query)
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