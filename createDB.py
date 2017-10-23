"""
Creates the databse and the table fot the project.
"""
from os.path import isfile, getsize
import sqlite3

DB_NAME = 'bulletin_board.sqlite'
TABLE_NAME = 'messages'


def isSQLite3(filename):
    """
    Check id db already exist
    """

    if not isfile(filename):
        return False
    if getsize(filename) < 100: # SQLite database file header is 100 bytes
        return False

    with open(filename, 'rb') as fd:
        header = fd.read(100)

    return header[:16] == b'SQLite format 3\x00'

def createBulletinDB(db_name, table_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("""CREATE table {} (id       INTEGER PRIMARY KEY,
                                  subject  TEXT NOT NULL,
                                  sender   TEXT NOT NULL,
                                  reply_to INTEGER REFERENCES message,
                                  text     TEXT NOT NULL
                                  )
    """.format(table_name))
    print(table_name)
    conn.commit()
    conn.close()

if isSQLite3(DB_NAME):
    print("Database already exists!")
else:
    createBulletinDB(DB_NAME, TABLE_NAME)
       