#!/usr/bin/env python3
print("Content-type: text/html\n")

import cgitb, cgi
import sqlite3
import utils


cursor, conn = utils.connectDB(False)

form = cgi.FieldStorage()
reply_to = form.getvalue('reply_to')

print("""
<html>
    <head>
        <title>Compose Message</title>
    </head>
    <body>
        <h1>Compose Message</h1>

    <form action='save.cgi' method='POST'>
    """)

subject = ''
if reply_to is not None:
    print('<input type="hidden" name="reply_to" value="{}"'.format(reply_to))
    cursor.execute('SELECT subject FROM messages WHERE id = {}'.format(reply_to))
    subject = cursor.fetchone()[0]
    if not subject.startswith('Re: '):
        subject = 'Re: ' + subject

print("""
    <b>Subject:</b><br>
    <input type='text' size='60' name='subject' value='{}' /><br>
    <b>Sender:</b><br>
    <input type='text' size='60' name='sender' /><br>
    <b>Message:</b><br>
    <textarea name='text' cols='60' rows='30'></textarea>
    <input type='submit' value='Save' />
    </form>
    <hr>
    <a href='main.cgi'>Back to the main page</a>
</body>
</html>
""".format(subject))