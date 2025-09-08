import os
import time
from datetime import datetime
import requests
import telebot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(BOT_TOKEN)

url = "https://api.binance.com/api/v3/ticker/price"
params = {"symbol": "SOLUSDT"}

last_price = None

while True:
    try:
        response = requests.get(url, params=params)
        data = response.json()
        price = float(data["price"])

        if last_price is None:
            last_price = price
            bot.send_message(CHAT_ID, f"Стартовый курс SOL/USDT: {price:.2f}")
            bot.send_message(CHAT_ID, f"Время: {datetime.now().strftime('%H:%M:%S %d.%m.%y')}")
            print(f"Стартовый курс SOL/USDT: {price:.2f}")
            print(datetime.now().strftime('%H:%M:%S %d.%m.%y'))
        else:
            diff = abs(price - last_price)
            if diff >= 1 and price > last_price:
                bot.send_message(
                    CHAT_ID,
                    f"🟢🔺 Курс ВЫРОС!\nБыло: {last_price:.2f}\nСтало: {price:.2f}\nИзменение: {diff:.2f} USDT"
                )
                print(f"🟢🔺 Курс ВЫРОС!\nБыло: {last_price:.2f}\nСтало: {price:.2f}\nИзменение: {diff:.2f} USDT")
                last_price = price
            elif diff >= 1 and price < last_price:
                bot.send_message(
                    CHAT_ID,
                    f"🔴🔻 Курс УПАЛ!\nБыло: {last_price:.2f}\nСтало: {price:.2f}\nИзменение: {diff:.2f} USDT"
                )
                print(f"🔴🔻 Курс УПАЛ!\nБыло: {last_price:.2f}\nСтало: {price:.2f}\nИзменение: {diff:.2f} USDT")
                last_price = price


        time.sleep(30)

    except Exception as e:
        bot.send_message(CHAT_ID, f"Ошибка: {e}")
        time.sleep(30)