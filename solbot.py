import os
import time
from datetime import datetime
import requests
import telebot
from dotenv import load_dotenv
from telebot.apihelper import ApiTelegramException

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(BOT_TOKEN)

url = "https://api.binance.com/api/v3/ticker/price"
params = {"symbol": "SOLUSDT"}

last_price = None


def safe_send_massage(chat_id, text, retries=3, dalay=5):
    for attempt in range(1, retries+1):
        try:
            bot.send_message(chat_id, text)
            return True
        except ApiTelegramException as e:
            print(f'⚠️ Ошибка Telegram (попытка {attempt}/{retries}): {e}')
            if attempt < retries:
                time.sleep(dalay)
        except Exception as e:
            print(f"❌ Непредвиденная ошибка при отправке: {e}")
            break
        print('🚫 Не удалось отправить сообщение в Telegram.')
        return False


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
                    f"🟢🔺 Курс ВЫРОС!\nСтало: {price:.2f}\nБыло: {last_price:.2f}\nИзменение: {diff:.2f} USDT")
                print(f"🟢🔺 Курс ВЫРОС!\nСтало: {price:.2f}\nБыло: {last_price:.2f}\nИзменение: {diff:.2f} USDT")
                last_price = price
            elif diff >= 1 and price < last_price:
                bot.send_message(
                    CHAT_ID,
                    f"🔴🔻 Курс УПАЛ!\nСтало: {price:.2f}\nБыло: {last_price:.2f}\nИзменение: {diff:.2f} USDT")
                print(f"🔴🔻 Курс УПАЛ!\nСтало: {price:.2f}\nБыло: {last_price:.2f}\nИзменение: {diff:.2f} USDT")
                last_price = price

        time.sleep(60)

    except Exception as e:
        bot.send_message(CHAT_ID, f"Ошибка: {e}")
        time.sleep(60)