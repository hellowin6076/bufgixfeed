import requests
from bs4 import BeautifulSoup
from logger import get_send_logger

async def send_google_trends(bot, chat_id):
    res = requests.get('https://zum.com/', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    soup = BeautifulSoup(res.text, 'html.parser')
    keywords = soup.find_all('span', class_='issue-word-list__keyword')

    message = "📈 *줌 이슈트렌드 TOP 10*\n"
    message += "━━━━━━━━━━━━━━━\n"
    for i, kw in enumerate(keywords[:10], 1):
        message += f"{i}. {kw.text.strip()}\n"

    get_send_logger().info(f"\n{message}")
    await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
