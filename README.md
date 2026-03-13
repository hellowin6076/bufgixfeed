# 📬 BufgixDailyBot

매일 아침 텔레그램으로 뉴스, 날씨, 트렌드 등을 전송하는 개인용 봇입니다.

## 📋 기능

| 기능 | 설명 | 스케줄 |
|------|------|--------|
| 🇰🇷 한국 뉴스 TOP 10 | Google News RSS | 매일 08:00 |
| 🇯🇵 일본 뉴스 TOP 10 | Google News RSS + 번역 | 매일 08:00 |
| 🌤 오사카 날씨 | OpenWeatherMap API | 매일 08:00 |
| 📈 이슈 트렌드 TOP 10 | 줌(zum.com) 스크래핑 | 매일 08:00 |
| 📺 유튜브 인기 TOP 10 | YouTube Data API v3 | 매일 08:00 |
| ⚽ EPL 경기 예고 | ESPN API | 매일 15:00 |
| 🎵 멜론 + Billboard TOP 30 | 스크래핑 | 매주 목요일 12:00 |
| 💱 원/엔/달러 환율 | exchangerate-api | 매주 월요일 08:00 |

## 🛠 기술 스택

- Python 3.12
- python-telegram-bot
- APScheduler
- BeautifulSoup4
- feedparser
- deep-translator

## ⚙️ 설치
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🔑 환경변수 설정

`.env` 파일 생성:
```
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
WEATHER_API_KEY=your_openweathermap_key
YOUTUBE_API_KEY=your_youtube_key
```

## 🚀 실행
```bash
nohup python main.py > /dev/null 2>&1 &
```

## 📁 로그

- `logs/bot.log` - 실행 로그
- `logs/send.log` - 전송 로그 (매주 월요일 로테이션, 영구 보관)
