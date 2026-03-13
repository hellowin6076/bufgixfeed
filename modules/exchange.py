import requests

async def send_exchange_rate(bot, chat_id):
    url = "https://api.exchangerate-api.com/v4/latest/KRW"
    res = requests.get(url).json()
    jpy = res["rates"]["JPY"]
    usd = res["rates"]["USD"]

    # 엔→원 계산 (1엔 = 1/jpy 원)
    krw_per_100jpy = (1 / jpy) * 100

    message = "💱 *이번 주 환율*\n"
    message += "━━━━━━━━━━━━━━━\n"
    message += f"🇰🇷 1,000원 → 🇯🇵 {jpy * 1000:.2f}엔\n"
    message += f"🇰🇷 10,000원 → 🇯🇵 {jpy * 10000:.2f}엔\n"
    message += f"🇯🇵 100엔 → 🇰🇷 {krw_per_100jpy:.2f}원\n"
    message += f"🇰🇷 10,000원 → 🇺🇸 ${usd * 10000:.4f}\n"
    await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
