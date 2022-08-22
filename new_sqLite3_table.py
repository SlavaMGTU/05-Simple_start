import sqlite3

con = sqlite3.connect(r'./db/db.db')


print ("Opened database successfully")
con.execute('''CREATE TABLE db
      (ID INT PRIMARY KEY     NOT NULL,
       barcode           TEXT    NOT NULL,
       name           TEXT    NOT NULL,
       qty            INT     NOT NULL;''')
print ("Table created successfully")
con.close()
