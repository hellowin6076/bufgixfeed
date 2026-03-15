import requests
from bs4 import BeautifulSoup
import billboard
from logger import get_send_logger

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

async def send_music_charts(bot, chat_id):
    await send_melon_chart(bot, chat_id)
    await send_billboard_chart(bot, chat_id)

async def send_melon_chart(bot, chat_id):
    res = requests.get('https://www.melon.com/chart/index.htm', headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')
    songs = soup.find_all('div', class_='ellipsis rank01')
    artists = soup.find_all('div', class_='ellipsis rank02')

    message = "🎵 멜론 차트 TOP 30\n"
    message += "━━━━━━━━━━━━━━━\n"
    for i, (s, a) in enumerate(zip(songs[:30], artists[:30]), 1):
        title = s.text.strip()
        artist_raw = a.text.strip()
        artist = artist_raw[:len(artist_raw)//2] if artist_raw[:len(artist_raw)//2] == artist_raw[len(artist_raw)//2:] else artist_raw
        message += f"{i}. {title} - {artist}\n"

    get_send_logger().info(f"\n{message}")
    await bot.send_message(chat_id=chat_id, text=message)

async def send_billboard_chart(bot, chat_id):
    chart = billboard.ChartData("hot-100")
    message = "🎵 Billboard Hot 100 TOP 30\n"
    message += "━━━━━━━━━━━━━━━\n"
    for i, entry in enumerate(chart[:30], 1):
        message += f"{i}. {entry.title} - {entry.artist}\n"
    get_send_logger().info(f"\n{message}")
    await bot.send_message(chat_id=chat_id, text=message)
