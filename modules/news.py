import feedparser
from deep_translator import GoogleTranslator
from logger import get_send_logger

KOREAN_NEWS_URL = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
JAPANESE_NEWS_URL = "https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja"

async def send_korean_news(bot, chat_id):
    feed = feedparser.parse(KOREAN_NEWS_URL)
    message = "🇰🇷 <b>한국 주요 뉴스 TOP 10</b>\n"
    message += "━━━━━━━━━━━━━━━\n"
    for i, entry in enumerate(feed.entries[:10], 1):
        message += f"{i}. {entry.title}\n"
        message += f"   🔗 {entry.link}\n\n"
    get_send_logger().info(f"\n{message}")
    await bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")

async def send_japanese_news(bot, chat_id):
    feed = feedparser.parse(JAPANESE_NEWS_URL)
    message = "🇯🇵 <b>일본 주요 뉴스 TOP 10 (번역)</b>\n"
    message += "━━━━━━━━━━━━━━━\n"
    for i, entry in enumerate(feed.entries[:10], 1):
        try:
            title = GoogleTranslator(source='ja', target='ko').translate(entry.title)
        except:
            title = entry.title
        message += f"{i}. {title}\n"
        message += f"   🔗 {entry.link}\n\n"
    get_send_logger().info(f"\n{message}")
    await bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
