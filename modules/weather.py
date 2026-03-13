import requests
import os

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CITY = "Osaka"

async def send_weather(bot, chat_id):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={WEATHER_API_KEY}&units=metric&lang=kr&cnt=8"
    res = requests.get(url).json()

    if res.get("cod") != "200":
        await bot.send_message(chat_id=chat_id, text="❌ 날씨 정보를 가져올 수 없습니다.")
        return

    message = "🌤 *오사카 날씨*\n"
    message += "━━━━━━━━━━━━━━━\n"

    for item in res["list"][:4]:
        time = item["dt_txt"][11:16]
        temp = item["main"]["temp"]
        feels = item["main"]["feels_like"]
        desc = item["weather"][0]["description"]
        humidity = item["main"]["humidity"]
        message += f"🕐 {time} | 🌡 {temp:.1f}°C (체감 {feels:.1f}°C)\n"
        message += f"   {desc} | 💧 습도 {humidity}%\n\n"

    await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
