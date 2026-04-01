import sqlite3

conn = sqlite3.connect("../crud_app_a/books.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM books")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
