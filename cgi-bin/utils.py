import cgitb
import os
import sqlite3

# Row factory
# It accepts the cursor and the original row as a tuple and will return the real result row.
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connectDB(fetchDict=True):
    #Remove before production deployment
    cgitb.enable()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__ + "/../"))
    db_path = os.path.join(BASE_DIR, 'bulletin_board.sqlite')

    conn = sqlite3.connect(db_path)
    
    if fetchDict:
        conn.row_factory = dict_factory

    return conn.cursor(), conn

def quote(string):
    if string:
        return string.replace("'", "\\")
    else:
        return string
