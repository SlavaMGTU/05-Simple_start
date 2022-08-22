import sqlite3

con = sqlite3.connect(r'./db/db.db')


print ("Opened database successfully")
cur=con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS db(barcode TEXT,'
                                          'name TEXT,'
                                          'qty INT)')
con.commit()
print ("Table created successfully")
cur.close()
con.close()
