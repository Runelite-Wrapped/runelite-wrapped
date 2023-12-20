# loads in sqlite db and lists the tables

import sqlite3

conn = sqlite3.connect("/stat.db")

c = conn.cursor()

c.execute("SELECT * FROM users")
print("hello")
print(c.fetchall())
