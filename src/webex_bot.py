# src/webex_bot.py
import os
import requests

WEBEX_TOKEN = os.getenv("WEBEX_BOT_TOKEN")
API_BASE = "https://webexapis.com/v1"

headers = {
    "Authorization": f"Bearer {WEBEX_TOKEN}",
    "Content-Type": "application/json"
}

def get_message(message_id: str):
    """Fetch full message details from Webex (text, personEmail, roomId)."""
    url = f"{API_BASE}/messages/{message_id}"
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()

def send_message(room_id: str, text: str):
    """Post a message into the room (where the candidate is)."""
    url = f"{API_BASE}/messages"
    payload = {"roomId": room_id, "text": text}
    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()
