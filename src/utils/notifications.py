import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_slack_notification(message: str, channel: str = None):
    """
    슬랙 Webhook을 통해 실시간 알림을 보냅니다.
    """
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("SLACK_WEBHOOK_URL not found in environment variables.")
        return

    payload = {
        "text": message
    }
    if channel:
        payload["channel"] = channel

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("Slack notification sent successfully.")
    except Exception as e:
        print(f"Error sending Slack notification: {e}")

if __name__ == "__main__":
    # send_slack_notification("DEAS 에이전트가 가동되었습니다. 🚀")
    pass
