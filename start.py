import os
import threading
from flask import Flask
from database import init_db

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running on Render!"

def run_bot():
    import main
    from funcs import bot
    bot.run()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
