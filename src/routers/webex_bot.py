# src/routers/webex_bot.py

import os
import requests
from fastapi import APIRouter, Request

# Simple in-memory interview state (POC only)
interview_state = {}

# Interview memory (temporary, in-memory)
ROOM_STATE = {}  # room_id -> last_question

FIRST_QUESTION = "👋 Hi! Welcome to the AI Interview.\n\nFirst question:\nTell me about yourself."



router = APIRouter()

WEBEX_TOKEN = os.getenv("WEBEX_BOT_TOKEN")
WEBEX_BOT_EMAIL = os.getenv("WEBEX_BOT_EMAIL")

API_BASE = "https://webexapis.com/v1"

headers = {
    "Authorization": f"Bearer {WEBEX_TOKEN}",
    "Content-Type": "application/json"
}

def get_message(message_id: str):
    """Fetch full message (text, personEmail, roomId)."""
    url = f"{API_BASE}/messages/{message_id}"
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()

def send_message(room_id: str, text: str):
    """Send message back to Webex user."""
    url = f"{API_BASE}/messages"
    payload = {"roomId": room_id, "text": text}
    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()


@router.post("/webhook")
async def webhook_handler(request: Request):
    """Webex will POST here whenever the user sends a message."""
    data = await request.json()

    # Extract message id
    message_id = data.get("data", {}).get("id")
    sender = data.get("data", {}).get("personEmail")

    # Ignore bot's own messages
    if sender == WEBEX_BOT_EMAIL:
        return {"status": "ignored - bot message"}

    # Get full message content
    msg = get_message(message_id)
    text = msg.get("text")
    person_email = msg.get("personEmail")
    room_id = msg.get("roomId")

    # If user wants to start interview
    if text.lower().strip() == "start interview":
        interview_state[room_id] = {
            "question": "Tell me about yourself."
        }
        send_message(room_id, "Interview started.\n\nQuestion 1: Tell me about yourself.")
        return {"status": "interview_started"}

# If interview already started
    # if room_id in interview_state:
    #     last_question = interview_state[room_id]["question"]

    #     reply = (
    #         f"Thanks for your answer.\n\n"
    #         f"Your answer was recorded.\n\n"
    #         f"Next question will come soon."
    #     )

    #     send_message(room_id, reply)
    #     return {"status": "answer_received"}

    # # Default fallback
    # send_message(room_id, f"You said: {text}")


    # return {"status": "ok"}

    # STEP 1: Start interview automatically
    if room_id not in interview_state:
        interview_state[room_id] = {
            "question": FIRST_QUESTION
        }
        send_message(room_id, FIRST_QUESTION)
        return {"status": "interview_started"}

    # STEP 2: Interview already in progress
    last_question = interview_state[room_id]["question"]

    # Simple evaluation placeholder (we'll improve later)
    next_question = (
        "Thank you for your answer.\n\n"
        "Next question:\n"
        "What are your key technical skills?"
    )

    send_message(room_id, next_question)

    # Update last question
    interview_state[room_id]["question"] = next_question

    return {"status": "next_question_sent"}

