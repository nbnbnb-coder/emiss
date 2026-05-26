from funcs import *
from balethon.conditions import equals

baned_users = [1493739055]


@bot.on_message(equals('/start'))
def s(message):
    if message.author.id in baned_users:
        message.reply("شما بن هستید❌")
        return 
    start(message)


@bot.on_message(equals("🎁 دریافت سود روزانه"))
def di(message):
    if message.author.id in baned_users:
        message.reply("شما بن هستید❌")
        return 
    daily_income(message)


# داشبورد
@bot.on_message(equals("📊 داشبورد", "🔄 به‌روزرسانی"))
def d(message):
    if message.author.id in baned_users:
        message.reply("شما بن هستید❌")
        return 
    dashboard(message)


@bot.on_message(equals("🏠 اصلی"))
def mm(message):
    if message.author.id in baned_users:
        message.reply("شما بن هستید❌")
        return 
    main_menu(message)


# ثبت کشور
@bot.on_message(equals("انتخاب کشور 🇮🇷"))
def sc(message):
    if message.author.id in baned_users:
        message.reply("شما بن هستید❌")
        return 
    set_country(message)

@bot.on_message(equals("💵 خرید سکه"))
def bm(message):
    if message.author.id in baned_users:
        message.reply("شما بن هستید❌")
        return 
    message.reply("""100 هزار سکه💰 10 هزار تومان💵

200 هزار سکه💰15 هزار تومان💵

400 هزار سکه 💰25 هزار تومان💵

500 هزار سکه 💰30 هزار تومان 💵

1 میلیون سکه💰45 هزار تومان 💵

2 میلیون سکه 💰50 هزار تومان💵

4 میلیون سکه 💰80 هزار تومان💵

برای خرید به @py_mc_amin مراجعه کنید""")


# اقتصاد
@bot.on_message(equals("💰 اقتصادی"))
def e(message):
    if message.author.id in baned_users:
        message.reply("شما بن هستید❌")
        return 
    economy(message)


# دفاع
@bot.on_message(equals("🛡 دفاعی"))
def d(message):
    if message.author.id in baned_users:
        message.reply("شما بن هستید❌")
        return 
    defense(message)


# حمله
@bot.on_message(equals("🚀 تهاجمی"))
def a(message):
    if message.author.id in baned_users:
        message.reply("شما بن هستید❌")
        return 
    attack(message)


@bot.on_message(equals("🚀 حمله"))
def am(message):
    if message.author.id in baned_users:
        message.reply("شما بن هستید❌")
        return 
    attack_menu(message)


# حمله جدید
@bot.on_message(equals("⚔️ حمله به کشورها"))
def sat(message):
    if message.author.id in baned_users:
        message.reply("شما بن هستید❌")
        return 
    show_attack_targets(message)

@bot.on_message(equals("📜 ارسال بیانیه"))
def wbm(message):
    if message.author.id in baned_users:
        message.reply("شما بن هستید❌")
        return 
    wait_bayanie_message(message)

@bot.on_message(equals("🎉 سکه رایگان"))
def rl(message):
    if message.author.id in baned_users:
        message.reply("شما بن هستید❌")
        return
    ref_link(message)


@bot.on_message()
def nc(message):
    if message.author.id in baned_users:
        message.reply("شما بن هستید❌")
        return 
    save_country(message)
    handle_attack_selection(message)
    handle_equipment_selection(message)
    buy_item(message)
    send_bayanie_message(message)


if __name__ == "__main__":
    bot.run()
