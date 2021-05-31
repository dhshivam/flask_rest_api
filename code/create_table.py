import sqlite3

db=sqlite3.connect("data.db")
cursor=db.cursor()

create_table="CREATE TABLE IF NOT EXISTS items (name text,price real)"
cursor.execute(create_table)

cursor.execute("INSERT INTO items VALUES ('test',20.0)")

db.commit()
db.close()