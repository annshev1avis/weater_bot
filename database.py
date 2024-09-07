import sqlite3

class Database:
    def __init__(self):
        self.con = sqlite3.connect("chat_city.db", check_same_thread=False)

    def disconnect(self):
        self.con.commit()
        self.con.close()

    def get_city(self, chat_id):
        cur = self.con.cursor()
        cur.execute(f"""select city from chat_city
                        where chat_id = {chat_id}
                        limit 1""")
        city = cur.fetchall()[0][0]
        cur.close()

        return city

    def update_chats_city(self, chat_id, city):
        cur = self.con.cursor()
        cur.execute(f"""delete from chat_city
                        where chat_id = {chat_id}""")
        cur.execute(f"""insert into chat_city
                        values({chat_id}, "{city}")""")
        self.con.commit()
        cur.close()

