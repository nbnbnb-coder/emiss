from balethon import *
from game import *

bot = Client("725516623:x5XGwJBLoaUe2IWZDWyLitE0G_RKcVz86XQ")

waiting_for_country = set()
waiting_for_attack = {}
waiting_for_bayanie = []


def start(message):
    user_id = message.author.id
    username = message.author.first_name

    user = get_user(user_id)

    if not (user and user["country"]):
        create_user(user_id, username)

        markup = types.ReplyKeyboard(
            ["انتخاب کشور 🇮🇷"],
            ["📊 داشبورد", "🏠 اصلی"]
        )
        bot.send_message(message.chat.id, "🎮 به بازی EMIS WAR خوش آمدید!\nابتدا کشور خود را انتخاب کنید:",
                         reply_markup=markup)
    else:
        markup = types.ReplyKeyboard(
            ["📊 داشبورد", "🏠 اصلی"]
        )
        bot.send_message(message.chat.id, "🎮 به بازی EMIS WAR خوش آمدید!",
                         reply_markup=markup)


def daily_income(message):
    user_id = message.author.id

    if user_id not in users:
        bot.send_message(message.chat.id, "ابتدا کشور خود را ثبت کنید.")
        return

    result = claim_daily_income(user_id)
    bot.send_message(message.chat.id, result["message"], reply_markup=get_main_menu())


# داشبورد

def dashboard(message):
    user_id = message.author.id
    user = get_user(user_id)

    if not user or not user['country']:
        message.reply("❌ ابتدا کشور را ثبت کنید!")
        return

    dashboard_text = get_dashboard_text(user)

    markup = types.ReplyKeyboard(
        ["🔄 به‌روزرسانی",
         "🏠 اصلی"]
    )

    message.reply(dashboard_text, reply_markup=markup)


def main_menu(message):
    message.reply("🏠 منوی اصلی EMIS WAR", reply_markup=get_main_menu())


# ثبت کشور

def set_country(message):
    waiting_for_country.add(message.author.id)
    message.reply("نام کشور یا لغو را وارد کنید:")


def save_country(message):
    user_id = message.author.id
    user = get_user(user_id)
    if user_id not in waiting_for_country:
        return

    if not message.text:
        message.reply("لطفاً فقط متن بفرست.")
        return

    if message.text == "لغو":
        waiting_for_country.remove(user_id)
        message.reply("ثبت کشور لغو شد.")
        return

    country_name = message.text.strip()
    if len(country_name) < 2 or len(country_name) > 30:
        message.reply("نام کشور باید بین 2 تا 30 کاراکتر باشد.")
        return
    create_user(user_id, user["name"], country_name)
    waiting_for_country.discard(user_id)
    message.reply("کشور ثبت شد.")


# اقتصاد

def economy(message):
    markup = types.ReplyKeyboard(
        ["🏢 بندر تجاری 22k", "🏭 کارخانه 35k"],
        ["🚂 ایستگاه 40k", "⛏️ معدن آهن 80k"],
        ["💎 الماس 100k", "🛢️ نفت 140k"],
        ["🏠 اصلی"]
    )
    message.reply("💰 بخش اقتصادی", reply_markup=markup)


# دفاع

def defense(message):
    markup = types.ReplyKeyboard(
        ["🛩️ زد هوایی 50k", "🚀 سراج 75k"],
        ["🔦 لیزری 100k", "🛡️ گنبد 150k"],
        ["🏠 اصلی"]
    )
    message.reply("🛡 بخش دفاعی", reply_markup=markup)


# حمله

def attack(message):
    markup = types.ReplyKeyboard(
        ["🚀 موشک 20k", "🛩️ پهپاد 25k"],
        ["✈️ F14 35k", "✈️ F15 50k"],
        ["✈️ F16 70k", "✈️ F35 100k"],
        ["🏠 اصلی"]
    )
    message.reply("🚀 بخش تهاجمی", reply_markup=markup)


def attack_menu(message):
    user_id = message.author.id

    if user_id not in users:
        bot.send_message(message.chat.id, "ابتدا کشور خود را ثبت کنید.")
        return

    keyboard = types.ReplyKeyboard(["⚔️ حمله به کشورها", "🏠 اصلی"])

    bot.send_message(message.chat.id, "یکی از گزینه‌های تهاجمی را انتخاب کنید:", reply_markup=keyboard)


# حمله جدید

def show_attack_targets(message):
    user_id = message.author.id

    if user_id not in users:
        bot.send_message(message.chat.id, "ابتدا کشور خود را ثبت کنید.")
        return

    targets = get_attackable_countries(user_id)

    if not targets:
        bot.send_message(message.chat.id, "فعلاً هیچ کشور دیگری برای حمله وجود ندارد.", reply_markup=get_main_menu())
        return

    waiting_for_attack[user_id] = {}

    keyboard = types.ReplyKeyboard()
    for t in targets:
        keyboard.add_row(f"{t[1]} | {t[0]}\n")

    bot.send_message(
        message.chat.id,
        "کشور موردنظر را برای حمله انتخاب کنید.",
        reply_markup=keyboard
    )


def handle_attack_selection(message):
    user_id = message.author.id
    text = message.text.strip()

    if user_id not in waiting_for_attack:
        return

    if text == "لغو":
        waiting_for_attack.pop(user_id)
        bot.send_message(message.chat.id, "حمله لغو شد.", reply_markup=get_main_menu())
        return

    if " | " not in text:
        bot.send_message(message.chat.id, "فرمت انتخاب نادرست است. دوباره انتخاب کنید یا لغو بزنید.")
        return

    try:
        country_name, defender_id_str = text.rsplit(" | ", 1)
        defender_id = int(defender_id_str)

        equipment_options = get_attack_equipment_options(user_id)
        if not equipment_options:
            waiting_for_attack.pop(user_id)
            bot.send_message(message.chat.id, "تجهیزات تهاجمی ندارید. ابتدا تجهیزات بخرید.",
                             reply_markup=get_main_menu())
            return

        waiting_for_attack[user_id] = {"defender_id": defender_id, "step": "equipment_selection"}

        keyboard = types.ReplyKeyboard()
        for eq in equipment_options:
            keyboard.add_row(eq)

        bot.send_message(message.chat.id, "تجهیز موردنظر برای حمله را انتخاب کنید", reply_markup=keyboard)

    except:
        bot.send_message(message.chat.id, "انتخاب معتبر نیست.")


def handle_equipment_selection(message):
    user_id = message.author.id
    text = message.text.strip()

    if user_id not in waiting_for_attack or waiting_for_attack[user_id]["step"] != "equipment_selection":
        return

    if text == "لغو":
        waiting_for_attack.pop(user_id)
        bot.send_message(message.chat.id, "حمله لغو شد.", reply_markup=get_main_menu())
        return

    equipment_options = get_attack_equipment_options(user_id)
    if text not in equipment_options:
        bot.send_message(message.chat.id, "تجهیز انتخابی معتبر نیست. دوباره تلاش کنید یا لغو کنید.")
        return

    defender_id = waiting_for_attack[user_id]["defender_id"]

    # اینجا تابع حمله و نبرد را صدا می‌زنیم، با تجهیزات انتخابی:
    result = attack_country_with_equipment(user_id, defender_id, text, bot)
    waiting_for_attack.pop(user_id)

    bot.send_message(message.chat.id, result["message"], reply_markup=get_main_menu())


def wait_bayanie_message(message):
    if message.author.id in waiting_for_bayanie:
        waiting_for_bayanie.remove(message.author.id)
    waiting_for_bayanie.append(message.author.id)
    bot.send_message(message.chat.id, "بیانیه رو بنویس تا در @bianieemisjang ارسال بشه📜")


def send_bayanie_message(message):
    user_id = message.author.id
    if not (user_id in waiting_for_bayanie):
        return
    waiting_for_bayanie.remove(user_id)
    bot.send_message(message.chat.id, "بیانیه ارسال شد✅")
    bot.send_message("@bianieemisjang", get_bayanie_text(user_id, message.text))

def ref_link(message):
    message.reply("لینک خود را از @EMISJANGREFBOT بگیرید")


# تابع خرید

def buy_item(message):
    user_id = message.author.id
    item = message.text

    # لیست کامل تجهیزات با قدرت و نوع
    equipments = {
        # اقتصاد
        "🏢 بندر تجاری 22k": {'name': 'بندر تجاری', 'price': 22000, 'power': 10000, 'type': 'economy'},
        "🏭 کارخانه 35k": {'name': 'کارخانه', 'price': 35000, 'power': 14000, 'type': 'economy'},
        "🚂 ایستگاه 40k": {'name': 'ایستگاه قطار', 'price': 40000, 'power': 19000, 'type': 'economy'},
        "⛏️ معدن آهن 80k": {'name': 'معدن آهن', 'price': 80000, 'power': 24000, 'type': 'economy'},
        "💎 الماس 100k": {'name': 'معدن الماس', 'price': 100000, 'power': 35000, 'type': 'economy'},
        "🛢️ نفت 140k": {'name': 'چاه نفت', 'price': 140000, 'power': 40000, 'type': 'economy'},

        # دفاع
        "🛩️ زد هوایی 50k": {'name': 'زد هوایی', 'price': 50000, 'power': 10000, 'type': 'defense'},
        "🚀 سراج 75k": {'name': 'پدافند سراج', 'price': 75000, 'power': 20000, 'type': 'defense'},
        "🔦 لیزری 100k": {'name': 'پدافند لیزری', 'price': 100000, 'power': 25000, 'type': 'defense'},
        "🛡️ گنبد 150k": {'name': 'گنبد آهنین', 'price': 150000, 'power': 35000, 'type': 'defense'},

        # حمله
        "🚀 موشک 20k": {'name': 'موشک بالستیک', 'price': 20000, 'power': 10000, 'type': 'attack'},
        "🛩️ پهپاد 25k": {'name': 'پهپاد شاهد', 'price': 25000, 'power': 15000, 'type': 'attack'},
        "✈️ F14 35k": {'name': 'اف-14', 'price': 35000, 'power': 35000, 'type': 'attack'},
        "✈️ F15 50k": {'name': 'اف-15', 'price': 50000, 'power': 45000, 'type': 'attack'},
        "✈️ F16 70k": {'name': 'اف-16', 'price': 70000, 'power': 55000, 'type': 'attack'},
        "✈️ F35 100k": {'name': 'اف-35', 'price': 100000, 'power': 70000, 'type': 'attack'}
    }

    if item in equipments:
        result = buy_equipment(
            user_id,
            equipments[item]['type'],
            equipments[item]['name'],
            equipments[item]['price'],
            equipments[item]['power']
        )
        message.reply(result["message"])
        if result['success']:
            dashboard(message)
