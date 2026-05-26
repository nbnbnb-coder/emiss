from balethon import Client
from balethon.conditions import private
from balethon.objects import ReplyKeyboard
import json
import os
from game import update_treasury
from datetime import datetime

bot = Client("1336859653:qpSnjhzlOwnOpMNMzNKOB0RyByGTRIvrops")

DATA_FILE = "referrals.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}, "referrals": {}}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"users": {}, "referrals": {}}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


data = load_data()


@bot.on_command(private)
async def start(referrer=None, *, client, message):
    reply = ReplyKeyboard(["گرفتن لینک"])

    user_id = str(message.author.id)
    # استفاده از فیلدهای درخواستی
    first_name = message.author.first_name or "کاربر"
    username = message.author.username or "بدون نام کاربری"

    # جلوگیری از ثبت مجدد
    if user_id in data["users"]:
        await message.reply(f"سلام {first_name} عزیز!\nشما قبلاً در ربات ثبت شده‌اید.", reply_markup=reply)
        return

    # ثبت اطلاعات کاربر جدید
    data["users"][user_id] = {
        "first_name": first_name,
        "username": username,
        "joined_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "referrer": referrer if referrer != user_id else None
    }

    # اگر رفرال معتبر بود و خودش نبود
    if referrer and str(referrer) != user_id:
        ref_id = str(referrer)
        if ref_id not in data["referrals"]:
            data["referrals"][ref_id] = {"count": 0, "invited_users": []}

        data["referrals"][ref_id]["count"] += 1
        update_treasury(int(ref_id), 50000)
        data["referrals"][ref_id]["invited_users"].append(user_id)

        await message.reply(f"🎉 خوش آمدید {first_name}!\nشما با لینک دعوت یکی از کاربران وارد شدید.", reply_markup=reply)
        await bot.send_message(referrer, f"یک زیر مجموعه به شما اضافه شد و ۵۰ هزار سکه گرفتید🎉")
    else:
        await message.reply(f"سلام {first_name}!\nخوش آمدید.", reply_markup=reply)

    save_data(data)


@bot.on_message(private)
async def answer_message(*, client, message):
    first_name = message.author.first_name or "کاربر"
    user_id = str(message.author.id)

    # ساخت لینک دعوت
    referral_link = client.create_referral_link("start", message.author.id)

    # دریافت تعداد دعوت‌ها
    ref_count = 0
    if user_id in data["referrals"]:
        ref_count = data["referrals"][user_id]["count"]

    await message.reply(
        f"سلام {first_name} عزیز 👋\n\n"
        f"لینک ربات بازی : @EMISJANGBOT\n\n"
        f"لینک دعوت اختصاصی شما:\n{referral_link}\n\n"
        f"تعداد دعوت‌های موفق شما: {ref_count} نفر"
    )


bot.run()
