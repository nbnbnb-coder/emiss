import sqlite3
import json
from datetime import datetime


# ایجاد دیتابیس
def init_db():
    conn = sqlite3.connect('emis_war.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        country TEXT,
        score INTEGER DEFAULT 0,
        treasury INTEGER DEFAULT 0,
        daily_profit INTEGER DEFAULT 0,
        defense INTEGER DEFAULT 0,
        attack_power INTEGER DEFAULT 0,
        war_status BOOLEAN DEFAULT 1,
        gift_status BOOLEAN DEFAULT 0,
        equip_defense TEXT DEFAULT '[]',
        equip_attack TEXT DEFAULT '[]',
        equip_economy TEXT DEFAULT '[]',
        last_login TEXT
    )''')
    conn.commit()
    conn.close()


init_db()


# دریافت اطلاعات کاربر
def get_user():
    conn = sqlite3.connect('emis_war.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    result = c.fetchall()
    conn.close()
    if result:
        users = {}
        for i in range(len(result)):
            user_id = result[i][0]
            users[user_id] = {
                'name': result[i][1], 'country': result[i][2],
                'score': result[i][3], 'treasury': result[i][4], 'daily_profit': result[i][5],
                'defense': result[i][6], 'attack': result[i][7], 'war': bool(result[i][8]),
                'gift': bool(result[i][9]), 'equip_defense': json.loads(result[i][10]),
                'equip_attack': json.loads(result[i][11]), 'equip_economy': json.loads(result[i][12])
            }
        return users
    return None


# ذخیره کاربر
def save_user(user_data):
    conn = sqlite3.connect('emis_war.db')
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO users 
        (user_id, name, country, score, treasury, daily_profit, defense, attack_power, 
         war_status, gift_status, equip_defense, equip_attack, equip_economy, last_login)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (user_data['user_id'], user_data['name'], user_data['country'],
               user_data['score'], user_data['treasury'], user_data['daily_profit'],
               user_data['defense'], user_data['attack'], user_data['war'],
               user_data['gift'], json.dumps(user_data['equip_defense']),
               json.dumps(user_data['equip_attack']), json.dumps(user_data['equip_economy']),
               datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
