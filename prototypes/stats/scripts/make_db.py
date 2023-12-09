# Script that just makes an sqlitedb for testing purposes

import sqlite3

conn = sqlite3.connect("my_database.db")

c = conn.cursor()

# Create blogs table
c.execute(
    """
          CREATE TABLE blogs
          (id INTEGER PRIMARY KEY,
           name TEXT,
           author TEXT)
          """
)

# Create posts table with a foreign key referencing blogs
c.execute(
    """
          CREATE TABLE posts
          (id INTEGER PRIMARY KEY,
           title TEXT,
           content TEXT,
           blog_id INTEGER,
           FOREIGN KEY(blog_id) REFERENCES blogs(id))
          """
)

# Insert some data into blogs
c.execute("INSERT INTO blogs VALUES (1, 'Python', 'Guido van Rossum')")
c.execute("INSERT INTO blogs VALUES (2, 'Data Science', 'Wes McKinney')")

# Insert post data with blog_id foreign key
c.execute(
    "INSERT INTO posts VALUES (1, 'Intro to Python', 'This post provides an intro to Python...', 1)"
)
c.execute(
    "INSERT INTO posts VALUES (2, 'Pandas Tutorial', 'This Pandas tutorial covers the basics...', 2)"
)

conn.commit()

print("Database created and populated with data!")

conn.close()
