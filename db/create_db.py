import sqlite3

con = sqlite3.connect('../patterns.sqlite')
cur = con.cursor()
with open('create_db.sql', 'r') as f:
    text = f.read()
    print(text)
cur.executescript(text)
cur.close()
con.close()
