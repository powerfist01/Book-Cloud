import sqlite3
conn=sqlite3.connect("book.db")
conn.execute("""
    CREATE TABLE BOOKS 
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT NOT NULL,
    COUNT INT)
    """)
print("Table Created!!!")
conn.close()