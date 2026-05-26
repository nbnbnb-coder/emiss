import os
import threading
from flask import Flask

import main
from funcs import bot

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running on Render!"

def run_bot():
    bot.run()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
