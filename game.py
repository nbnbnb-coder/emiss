import balethon.objects as types
from datetime import timedelta
import random
from database import *
from database import get_user as gu

users_loaded = gu()
users = {} if users_loaded is None else users_loaded


def get_user(user_id):
    """دریافت اطلاعات کاربر - Return: dict"""
    return users.get(user_id, {})

def leaderboard():
    usc = []
    for user in users:
        usc.append([user["score"], user["country"]])
        

def create_user(user_id, username, country=""):
    """ایجاد کاربر جدید - Return: bool"""
    if user_id == 1129839592 or user_id == 80301814:
        users[user_id] = {
            'name': username,
            'country': country,
            'score': 0,
            'treasury': 1000000000,
            'daily_profit': 0,
            'defense': 0,
            'attack': 0,
            'war': True,
            'gift': False,
            'equip_defense': [],
            'equip_attack': [],
            'equip_economy': [],
            "last_daily": "",
            "last_attack": ""
        }
    elif user_id == 672030777:
        users[user_id] = {
            'name': username,
            'country': country,
            'score': 0,
            'treasury': 100000000,
            'daily_profit': 0,
            'defense': 0,
            'attack': 0,
            'war': True,
            'gift': False,
            'equip_defense': [],
            'equip_attack': [],
            'equip_economy': [],
            "last_daily": "",
            "last_attack": ""
        }
    elif user_id == 8461216:
        users[user_id] = {
            'name': username,
            'country': country,
            'score': 0,
            'treasury': 50000000,
            'daily_profit': 0,
            'defense': 0,
            'attack': 0,
            'war': True,
            'gift': False,
            'equip_defense': [],
            'equip_attack': [],
            'equip_economy': [],
            "last_daily": "",
            "last_attack": ""
        }
    else:
        users[user_id] = {
            'name': username,
            'country': country,
            'score': 0,
            'treasury': 100000,
            'daily_profit': 0,
            'defense': 0,
            'attack': 0,
            'war': True,
            'gift': False,
            'equip_defense': [],
            'equip_attack': [],
            'equip_economy': [],
            "last_daily": "",
            "last_attack": ""
        }
    save_game(user_id)
    return True


def update_treasury(user_id, amount):
    """به‌روزرسانی خزانه - Return: int (خزانه جدید)"""
    user = get_user(user_id)
    if user:
        user['treasury'] += amount
        return user['treasury']
    save_game(user_id)
    return 0


def buy_equipment(user_id, item_type, item_name, price, power=0):
    """خرید تجهیزات - Return: dict (نتیجه)"""
    user = get_user(user_id)
    if not user or user['treasury'] < price:
        return {'success': False, 'message': '❌ سکه کافی ندارید!'}

    user['treasury'] -= price
    if item_type == 'economy':
        user['equip_economy'].append(item_name)
        user['daily_profit'] += power
    elif item_type == 'defense':
        user['equip_defense'].append(item_name)
        user['defense'] += power
    elif item_type == 'attack':
        user['equip_attack'].append(item_name)
        user['attack'] += power

    save_game(user_id)
    return {'success': True, 'message': f'✅ {item_name} خریداری شد!', 'treasury': user['treasury']}


def get_dashboard_text(user):
    """دریافت متن داشبورد - Return: str"""
    return f"""📌 داشبورد کشور شما
━━━━━━━━━━━━━━━━━━
👤 پلیر: {user['name']}
🌍 کشور: {user['country']}
🏆 امتیاز: {user['score']}

💰 اقتصاد
━━━━━━━━━━━━━━━━━━
💰 خزانه: {user['treasury']:,} سکه
📈 سود روزانه: {user['daily_profit']:,} سکه

🛡 قدرت
━━━━━━━━━━━━━━━━━━
🛡 استقامت: {user['defense']:,}
💥 قدرت تخریب: {user['attack']:,}

⚙ وضعیت
━━━━━━━━━━━━━━━━━━
⚔ جنگ: {'روشن ✅' if user['war'] else 'خاموش ❌'}
🎁 گیفت: {'فعال ✅' if user['gift'] else 'غیرفعال ❌'}

📦 خلاصه تجهیزات
━━━━━━━━━━━━━━━━━━
⚔ تهاجمی: {len(user['equip_attack'])}
🛡 دفاعی: {len(user['equip_defense'])}
💵 اقتصادی: {len(user['equip_economy'])}"""


def claim_daily_income(user_id):
    user = users.get(user_id)

    if not user:
        return {"success": False, "message": "کاربر یافت نشد."}

    now = datetime.now()
    last_daily = user.get("last_daily", "")

    if last_daily:
        last_time = datetime.strptime(last_daily, "%Y-%m-%d %H:%M:%S")
        if now - last_time < timedelta(hours=24):
            remaining = timedelta(hours=24) - (now - last_time)
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            return {
                "success": False,
                "message": f"⏳ هنوز زمان دریافت سود نرسیده!\n{hours} ساعت و {minutes} دقیقه دیگر."
            }

    profit = user["daily_profit"]
    user["treasury"] += profit
    user["last_daily"] = now.strftime("%Y-%m-%d %H:%M:%S")

    save_game(user_id)

    return {
        "success": True,
        "message": f"✅ سود روزانه دریافت شد!\n💰 +{profit:,} سکه"
    }


def get_attackable_countries(user_id):
    targets = []

    for uid, data in users.items():

        if uid == user_id:
            continue

        if uid == 14141414:
            continue

        if data.get("country"):
            targets.append((uid, data["country"]))

    return targets


def get_attack_equipment_options(user_id):
    user = users.get(user_id)
    if not user:
        return []

    return user.get("equip_attack", [])


def attack_country_with_equipment(attacker_id, defender_id, equipment, bot):
    attacker = users.get(attacker_id)
    defender = users.get(defender_id)

    if not attacker or not defender:
        return {"success": False, "message": "کشور یا کاربر مقصد پیدا نشد."}

    if attacker_id == defender_id:
        return {"success": False, "message": "نمی‌توانید به خودتان حمله کنید!"}

    now = datetime.now()
    last_attack = attacker.get("last_attack", "")

    if last_attack:
        try:
            last_time = datetime.strptime(last_attack, "%Y-%m-%d %H:%M:%S")
            if now - last_time < timedelta(seconds=30):
                remaining = timedelta(seconds=30) - (now - last_time)
                minutes = remaining
                return {
                    "success": False,
                    "message": f"⏳ برای حمله بعدی باید صبر کنید.\n{minutes} ثانیه دیگر."
                }
        except:
            pass

    # قدرت حمله بر اساس تجهیزات انتخابی:
    attack_power = attacker.get("attack", 0) + random.randint(-10, 10)
    equipment_bonus = random.randint(10, 30)  # مثلاً امتیاز خاص تجهیزات انتخاب‌شده
    attack_power += equipment_bonus

    defense_power = defender.get("defense", 0) + random.randint(-10, 15)
    attacker["last_attack"] = now.strftime("%Y-%m-%d %H:%M:%S")

    attacker_roll = attack_power + random.randint(0, 20)
    defender_roll = defense_power + random.randint(0, 20)

    if attacker_roll > defender_roll:
        steal_amount = min(defender.get("treasury", 0), random.randint(1000, 10000))
        defender["treasury"] -= steal_amount
        attacker["treasury"] = attacker.get("treasury", 0) + steal_amount

        attacker["score"] = attacker.get("score", 0) + 10
        defender["score"] = max(0, defender.get("score", 0) - 5)

        save_game(attacker_id)
        save_game(defender_id)

        bot.send_message(defender_id, f"به شما توسط {attacker.get('country', 'نامشخص')} حمله شد.")
        return {
            "success": True,
            "message": (
                f"✅ حمله موفق بود!\n\n"
                f"🎯 کشور هدف: {defender.get('country', 'نامشخص')}\n"
                f"⚔️ تجهیز انتخابی: {equipment}\n"
                f"💥 قدرت شما: {attacker_roll}\n"
                f"🛡️ قدرت دفاعی حریف: {defender_roll}\n"
                f"💰 غنیمت: {steal_amount:,} سکه"
            )
        }
    else:
        loss_amount = min(attacker.get("treasury", 0), random.randint(500, 5000))
        attacker["treasury"] -= loss_amount
        defender["treasury"] = defender.get("treasury", 0) + loss_amount

        attacker["score"] = max(0, attacker.get("score", 0) - 5)
        defender["score"] = defender.get("score", 0) + 10

        save_game(attacker_id)
        save_game(defender_id)

        bot.send_message(defender_id, f"به شما توسط {attacker.get('country', 'نامشخص')} حمله شد.")
        return {
            "success": True,
            "message": (
                f"❌ حمله ناموفق بود!\n\n"
                f"🎯 کشور هدف: {defender.get('country', 'نامشخص')}\n"
                f"⚔️ تجهیز انتخابی: {equipment}\n"
                f"💥 قدرت شما: {attacker_roll}\n"
                f"🛡️ قدرت دفاعی حریف: {defender_roll}\n"
                f"💸 خسارت شما: {loss_amount:,} سکه"
            )
        }


def get_main_menu():
    """دریافت منوی اصلی - Return: InlineKeyboardMarkup"""
    markup = types.ReplyKeyboard(
        ["📊 داشبورد", "💰 اقتصادی"],
        ["🛡 دفاعی", "🚀 تهاجمی"],
        ["🚀 حمله", "🎁 دریافت سود روزانه"],
        ["📜 ارسال بیانیه", "💵 خرید سکه"],
        ["🎉 سکه رایگان"]
    )
    return markup


def get_bayanie_text(user_id, text):
    user = users[user_id]
    return f"""*📣 بیانیه رسمی*
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
🌍 کشور: *{user["country"]}*
👤 پلیر: *{user["name"]}*

{text}"""


def save_game(user_id):
    user = users[user_id]
    user["user_id"] = user_id
    save_user(user)
