import os
import asyncio
import traceback
from dotenv import load_dotenv
from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from logger import setup_loggers
from modules.news import send_korean_news, send_japanese_news
from modules.weather import send_weather
from modules.football import send_football_preview
from modules.music import send_music_charts
from modules.youtube import send_youtube_trends
from modules.trends import send_google_trends
from modules.exchange import send_exchange_rate

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

run_logger, send_logger = setup_loggers(BOT_TOKEN, CHAT_ID)

bot = Bot(token=BOT_TOKEN)
scheduler = AsyncIOScheduler(timezone="Asia/Tokyo")

async def morning_briefing():
    send_logger.info("📨 모닝 브리핑 전송 시작")
    try:
        await send_korean_news(bot, CHAT_ID)
        send_logger.info("✅ 한국 뉴스 전송 완료")
        await send_japanese_news(bot, CHAT_ID)
        send_logger.info("✅ 일본 뉴스 전송 완료")
        await send_weather(bot, CHAT_ID)
        send_logger.info("✅ 날씨 전송 완료")
        await send_google_trends(bot, CHAT_ID)
        send_logger.info("✅ 트렌드 전송 완료")
        await send_youtube_trends(bot, CHAT_ID)
        send_logger.info("✅ 유튜브 전송 완료")
        send_logger.info("🎉 모닝 브리핑 전송 완료")
    except Exception as e:
        send_logger.error(f"모닝 브리핑 오류: {traceback.format_exc()}")

async def football_preview():
    try:
        send_logger.info("⚽ EPL 경기 예고 전송 시작")
        await send_football_preview(bot, CHAT_ID)
        send_logger.info("✅ EPL 경기 예고 전송 완료")
    except Exception as e:
        send_logger.error(f"EPL 경기 예고 오류: {traceback.format_exc()}")

async def music_charts():
    try:
        send_logger.info("🎵 음악 차트 전송 시작")
        await send_music_charts(bot, CHAT_ID)
        send_logger.info("✅ 음악 차트 전송 완료")
    except Exception as e:
        send_logger.error(f"음악 차트 오류: {traceback.format_exc()}")

async def exchange_rate():
    try:
        send_logger.info("💱 환율 전송 시작")
        await send_exchange_rate(bot, CHAT_ID)
        send_logger.info("✅ 환율 전송 완료")
    except Exception as e:
        send_logger.error(f"환율 오류: {traceback.format_exc()}")

def setup_scheduler():
    scheduler.add_job(morning_briefing, "cron", hour=8, minute=0)
    scheduler.add_job(football_preview, "cron", hour=15, minute=0)
    scheduler.add_job(music_charts, "cron", day_of_week="thu", hour=12, minute=0)
    scheduler.add_job(exchange_rate, "cron", day_of_week="mon", hour=8, minute=0)

async def main():
    setup_scheduler()
    scheduler.start()
    run_logger.info("🤖 봇 시작!")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
