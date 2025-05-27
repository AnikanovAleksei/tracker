import requests
from django.conf import settings


def send_telegram_message(chat_id: int, message: str) -> bool:
    url = f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage"
    try:
        response = requests.post(
            url,
            json={
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'Markdown'
            },
            timeout=5
        )
        return response.ok
    except requests.RequestException:
        return False
