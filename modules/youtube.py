import requests
import os

async def send_youtube_trends(bot, chat_id):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet",
        "chart": "mostPopular",
        "regionCode": "KR",
        "maxResults": 10,
        "key": os.getenv("YOUTUBE_API_KEY")
    }
    res = requests.get(url, params=params).json()
    if "items" not in res:
        print("API 오류:", res)
        await bot.send_message(chat_id=chat_id, text="유튜브 데이터를 가져오지 못했어요.")
        return
    message = "📺 유튜브 한국 인기 동영상 TOP 10\n"
    message += "━━━━━━━━━━━━━━━\n"
    for i, item in enumerate(res["items"], 1):
        title = item["snippet"]["title"]
        channel = item["snippet"]["channelTitle"]
        video_id = item["id"]
        message += f"{i}. {title}\n"
        message += f"   📺 {channel} | 🔗 https://youtu.be/{video_id}\n\n"
    await bot.send_message(chat_id=chat_id, text=message)
