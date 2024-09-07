"""запускается только один раз - для создания БД"""

import sqlite3 as sq

con = sq.connect("chat_city.db")
cur = con.cursor()

cur.execute(""" create table if not exists chat_city(
                chat_id integer,
                city text
                )""")

cur.close()
con.commit()
con.close()