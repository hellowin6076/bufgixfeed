import requests
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))

async def send_football_preview(bot, chat_id):
    url = 'https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard'
    res = requests.get(url).json()
    events = res.get('events', [])

    if not events:
        return

    message = "⚽ *EPL 오늘의 경기*\n"
    message += "━━━━━━━━━━━━━━━\n"

    liverpool_lines = []
    other_lines = []

    for event in events:
        name = event['name']
        utc_time = datetime.strptime(event['date'], "%Y-%m-%dT%H:%MZ").replace(tzinfo=timezone.utc)
        kst_time = utc_time.astimezone(KST).strftime("%H:%M")
        status = event['status']['type']['description']

        if 'Liverpool' in name:
            liverpool_lines.append(f"🔴 {name}\n   🕐 {kst_time} KST | {status}")
        else:
            other_lines.append(f"⚪ {name}\n   🕐 {kst_time} KST | {status}")

    if not liverpool_lines and not other_lines:
        return

    for line in liverpool_lines:
        message += line + "\n\n"
    for line in other_lines:
        message += line + "\n\n"

    await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
