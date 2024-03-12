#НИЧЕГО ТУТ НЕ МЕНЯТЬ

import sqlite3 as sq

db = sq.connect('bd')
cursor = db.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS promos(
promos_name TEXT
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS used_promos(
used_promos_name TEXT
)""")


cursor.execute("""CREATE TABLE IF NOT EXISTS nicks(
name TEXT,
good_time INTEGER
)""")

cursor.close()
db.commit() 
db.close()

#если случайно удалите базу - просто запустите этот код
