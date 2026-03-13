import logging
import os
from datetime import date
from logging.handlers import TimedRotatingFileHandler

os.makedirs("logs", exist_ok=True)

class TelegramErrorHandler(logging.Handler):
    def __init__(self, token, chat_id):
        super().__init__(level=logging.ERROR)
        self.token = token
        self.chat_id = chat_id
        self.sent_errors = {}

    def emit(self, record):
        try:
            import requests
            today = date.today()
            error_key = record.getMessage()[:100]
            if self.sent_errors.get(error_key) == today:
                return
            self.sent_errors[error_key] = today
            msg = self.format(record)
            text = f"🚨 *봇 에러 발생*\n```{msg}```"
            requests.post(
                f"https://api.telegram.org/bot{self.token}/sendMessage",
                json={"chat_id": self.chat_id, "text": text, "parse_mode": "Markdown"},
                timeout=5
            )
        except:
            pass

def setup_loggers(bot_token, chat_id):
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    tg_handler = TelegramErrorHandler(bot_token, chat_id)

    # 실행 로그
    run_logger = logging.getLogger("run")
    run_logger.setLevel(logging.INFO)
    run_handler = logging.FileHandler("logs/bot.log", encoding="utf-8")
    run_handler.setFormatter(formatter)
    run_logger.addHandler(run_handler)
    run_logger.addHandler(logging.StreamHandler())
    run_logger.addHandler(tg_handler)

    # 전송 로그
    send_logger = logging.getLogger("send")
    send_logger.setLevel(logging.INFO)
    send_handler = TimedRotatingFileHandler(
        "logs/send.log", when="W0", interval=1, backupCount=0, encoding="utf-8"
    )
    send_handler.setFormatter(formatter)
    send_logger.addHandler(send_handler)
    send_logger.addHandler(tg_handler)

    return run_logger, send_logger
