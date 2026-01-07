# # # src/routers/webex_bot.py

# import os
# import requests
# from fastapi import APIRouter, Request
# from src.agent import evaluate_and_next


# # In-memory interview memory (POC only)
# ROOM_STATE = {}  # room_id -> last_question

# FIRST_QUESTION = (
#     "👋 Hi! Welcome to the AI Interview.\n\n"
#     "First question:\n"
#     "Tell me about yourself."
# )

# SECOND_QUESTION = (
#     "Thank you for your answer! 👍\n\n"
#     "Next question:\n"
#     "What are your key technical skills?"
# )

# router = APIRouter()

# WEBEX_TOKEN = os.getenv("WEBEX_BOT_TOKEN")
# WEBEX_BOT_EMAIL = os.getenv("WEBEX_BOT_EMAIL")

# API_BASE = "https://webexapis.com/v1"

# headers = {
#     "Authorization": f"Bearer {WEBEX_TOKEN}",
#     "Content-Type": "application/json"
# }

# def get_message(message_id: str):
#     """Fetch full message (text, personEmail, roomId)."""
#     url = f"{API_BASE}/messages/{message_id}"
#     resp = requests.get(url, headers=headers, timeout=10)
#     resp.raise_for_status()
#     return resp.json()

# def send_message(room_id: str, text: str):
#     """Send message back to Webex user."""
#     url = f"{API_BASE}/messages"
#     payload = {
#         "roomId": room_id,
#         "text": text
#     }
#     resp = requests.post(url, json=payload, headers=headers, timeout=10)
#     resp.raise_for_status()
#     return resp.json()

# @router.post("/webhook")
# async def webhook_handler(request: Request):
#     """Webex will POST here whenever the user sends a message."""
#     data = await request.json()

#     message_id = data.get("data", {}).get("id")
#     sender = data.get("data", {}).get("personEmail")

#     # Ignore bot's own messages
#     if sender == WEBEX_BOT_EMAIL:
#         return {"status": "ignored_bot_message"}

#     # Fetch full message
#     msg = get_message(message_id)
#     text = msg.get("text", "").strip()
#     room_id = msg.get("roomId")

#     # STEP 1: Start interview (first message in room)
#     if room_id not in ROOM_STATE:
#         ROOM_STATE[room_id] = FIRST_QUESTION
#         send_message(room_id, FIRST_QUESTION)
#         return {"status": "interview_started"}

#     # # STEP 2: Interview already in progress
#     # last_question = ROOM_STATE[room_id]

#     # # For now, always ask second question (POC logic)
#     # ROOM_STATE[room_id] = SECOND_QUESTION
#     # send_message(room_id, SECOND_QUESTION)

#     # return {"status": "next_question_sent"}

#     # STEP 2: Interview already in progress
#     last_question = ROOM_STATE[room_id]

#     # Ask AI for next question
#     next_question = evaluate_and_next(
#         last_question=last_question,
#         answer_text=text
#     )

#     # Save and send
#     ROOM_STATE[room_id] = next_question
#     send_message(room_id, next_question)

#     return {"status": "next_question_sent"}


# src/routers/webex_bot.py

import os
import requests
from fastapi import APIRouter, Request

router = APIRouter()

WEBEX_TOKEN = os.getenv("WEBEX_BOT_TOKEN")
WEBEX_BOT_EMAIL = os.getenv("WEBEX_BOT_EMAIL")

API_BASE = "https://webexapis.com/v1"

headers = {
    "Authorization": f"Bearer {WEBEX_TOKEN}",
    "Content-Type": "application/json"
}

# -------------------------
# Interview State (POC)
# -------------------------
ROOM_STATE = {}

STAGE_INTRO = "INTRO"
STAGE_TECH = "TECH"
STAGE_HR = "HR"
STAGE_CLOSING = "CLOSING"
STAGE_COMPLETED = "COMPLETED"

FIRST_QUESTION = (
    "👋 Hi! Welcome to the AI Interview.\n\n"
    "Let’s begin.\n\n"
    "First question:\nTell me about yourself."
)

# -------------------------
# Webex Helpers
# -------------------------
def get_message(message_id: str):
    url = f"{API_BASE}/messages/{message_id}"
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()

def send_message(room_id: str, text: str):
    url = f"{API_BASE}/messages"
    payload = {"roomId": room_id, "text": text}
    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()

# -------------------------
# Webhook
# -------------------------
@router.post("/webhook")
async def webhook_handler(request: Request):
    data = await request.json()

    message_id = data.get("data", {}).get("id")
    sender = data.get("data", {}).get("personEmail")

    if sender == WEBEX_BOT_EMAIL:
        return {"status": "ignored_bot"}

    msg = get_message(message_id)
    text = msg.get("text", "").strip()
    room_id = msg.get("roomId")

    # -------------------------
    # INIT INTERVIEW
    # -------------------------
    if room_id not in ROOM_STATE:
        ROOM_STATE[room_id] = {
            "stage": STAGE_INTRO,
            "last_question": FIRST_QUESTION,
            "answers": [],
            "profile": {
                "experience": None,
                "current_ctc": None,
                "expected_ctc": None,
                "notice_period": None
            }
        }
        send_message(room_id, FIRST_QUESTION)
        return {"status": "interview_started"}

    state = ROOM_STATE[room_id]

    # Store answer
    state["answers"].append({
        "question": state["last_question"],
        "answer": text
    })

    # -------------------------
    # MOVE FROM INTRO → TECH
    # -------------------------
    if state["stage"] == STAGE_INTRO:
        next_question = "Great. Can you explain your current role and key responsibilities?"
        state["stage"] = STAGE_TECH
        state["last_question"] = next_question
        send_message(room_id, next_question)
        return {"status": "tech_started"}

    # -------------------------
    # TECH (placeholder)
    # -------------------------
    if state["stage"] == STAGE_TECH:
        next_question = "Thank you. We will continue with more technical questions shortly."
        state["last_question"] = next_question
        send_message(room_id, next_question)
        return {"status": "tech_continue"}

    return {"status": "ok"}
