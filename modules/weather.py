import requests
import os
import sqlite3
from datetime import datetime, timedelta
from logger import get_send_logger

CITY = "Osaka"
DB_PATH = "data/weather.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS weather_history (
        date TEXT PRIMARY KEY,
        temp_max REAL,
        temp_min REAL,
        feels_like REAL,
        humidity INTEGER,
        description TEXT
    )''')
    conn.commit()
    conn.close()

def save_today(temp_max, temp_min, feels_like, humidity, description):
    conn = sqlite3.connect(DB_PATH)
    today = datetime.now().strftime("%Y-%m-%d")
    conn.execute('''INSERT OR REPLACE INTO weather_history VALUES (?, ?, ?, ?, ?, ?)''',
        (today, temp_max, temp_min, feels_like, humidity, description))
    conn.commit()
    conn.close()

def load_yesterday():
    conn = sqlite3.connect(DB_PATH)
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    cur = conn.execute('SELECT * FROM weather_history WHERE date = ?', (yesterday,))
    row = cur.fetchone()
    conn.close()
    return row

def diff_str(today, yesterday, unit="°C"):
    diff = today - yesterday
    if diff > 0:
        return f"▲{abs(diff):.1f}{unit}"
    elif diff < 0:
        return f"▼{abs(diff):.1f}{unit}"
    else:
        return f"→ 동일"

async def send_weather(bot, chat_id):
    init_db()
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={api_key}&units=metric&lang=kr&cnt=8"
    res = requests.get(url).json()
    if res.get("cod") != "200":
        await bot.send_message(chat_id=chat_id, text="❌ 날씨 정보를 가져올 수 없습니다.")
        return

    items = res["list"][:4]
    temps = [i["main"]["temp"] for i in items]
    feels = [i["main"]["feels_like"] for i in items]
    humidities = [i["main"]["humidity"] for i in items]
    descriptions = [i["weather"][0]["description"] for i in items]

    temp_max = max(temps)
    temp_min = min(temps)
    feels_avg = sum(feels) / len(feels)
    humidity_avg = int(sum(humidities) / len(humidities))
    desc_today = descriptions[0]

    yesterday = load_yesterday()

    message = "🌤 *오사카 날씨*\n"
    message += "━━━━━━━━━━━━━━━\n"
    for item in items:
        time = item["dt_txt"][11:16]
        temp = item["main"]["temp"]
        feel = item["main"]["feels_like"]
        desc = item["weather"][0]["description"]
        humidity = item["main"]["humidity"]
        message += f"🕐 {time} | 🌡 {temp:.1f}°C (체감 {feel:.1f}°C)\n"
        message += f"   {desc} | 💧 습도 {humidity}%\n\n"

    message += "━━━━━━━━━━━━━━━\n"
    message += f"📊 *오늘 요약*\n"
    message += f"🌡 최고 {temp_max:.1f}°C / 최저 {temp_min:.1f}°C\n"
    message += f"🤔 평균 체감 {feels_avg:.1f}°C\n"
    message += f"💧 평균 습도 {humidity_avg}%\n"

    if yesterday:
        _, y_max, y_min, y_feels, y_humidity, y_desc = yesterday
        message += "\n📅 *어제 대비*\n"
        message += f"🌡 최고 {diff_str(temp_max, y_max)} / 최저 {diff_str(temp_min, y_min)}\n"
        message += f"🤔 체감 {diff_str(feels_avg, y_feels)}\n"
        message += f"💧 습도 {diff_str(humidity_avg, y_humidity, '%')}\n"
        if desc_today != y_desc:
            message += f"🌈 날씨 {y_desc} → {desc_today}\n"

    save_today(temp_max, temp_min, feels_avg, humidity_avg, desc_today)
    get_send_logger().info(f"\n{message}")
    await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
