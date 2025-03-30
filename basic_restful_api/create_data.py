import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("INSERT INTO users (name,email) VALUES ('Alice','alice@gmail.com')")
cursor.execute("INSERT INTO users (name,email) VALUES ('Bob','bob@gmail.com')")
conn.commit()
conn.close()