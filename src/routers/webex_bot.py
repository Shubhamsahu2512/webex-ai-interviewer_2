
# import os
# import requests
# from fastapi import APIRouter, Request
# #from src.utils.mailer import send_feedback_email
# from src.agent import generate_feedback
# from src.agents import ask_next_technical_question

# router = APIRouter()

# # -------------------------
# # ENV
# # -------------------------
# WEBEX_TOKEN = os.getenv("WEBEX_BOT_TOKEN")
# WEBEX_BOT_EMAIL = os.getenv("WEBEX_BOT_EMAIL")

# JOB_DESCRIPTION = """
# Role: Senior RPA Developer

# Required Skills:
# - Blue Prism
# - Python
# - REST APIs
# - Automation best practices
# - Exception handling
# - Orchestration and queues

# Responsibilities:
# - Design and develop enterprise-grade RPA solutions
# - Handle production issues
# - Work with business stakeholders
# """

# API_BASE = "https://webexapis.com/v1"

# headers = {
#     "Authorization": f"Bearer {WEBEX_TOKEN}",
#     "Content-Type": "application/json"
# }

# # -------------------------
# # CONSTANTS
# # -------------------------
# STAGE_INTRO = "INTRO"
# STAGE_TECH = "TECH"
# STAGE_HR = "HR"
# STAGE_COMPLETED = "COMPLETED"

# FIRST_QUESTION = (
#     "👋 Hi! Welcome to the AI Interview.\n\n"
#     "Let’s begin.\n\n"
#     "Tell me about yourself."
# )

# HR_QUESTIONS = [
#     "How many years of total professional experience do you have?",
#     "What is your current CTC (annual)?",
#     "What is your expected CTC?",
#     "What is your notice period (in days)?"
# ]

# # -------------------------
# # IN-MEMORY STATE (POC)
# # -------------------------
# ROOM_STATE = {}

# # -------------------------
# # WEBEX HELPERS
# # -------------------------
# def get_message(message_id: str):
#     url = f"{API_BASE}/messages/{message_id}"
#     resp = requests.get(url, headers=headers, timeout=10)
#     resp.raise_for_status()
#     return resp.json()

# def send_message(room_id: str, text: str):
#     url = f"{API_BASE}/messages"
#     payload = {"roomId": room_id, "text": text}
#     resp = requests.post(url, json=payload, headers=headers, timeout=10)
#     resp.raise_for_status()
#     return resp.json()

# # -------------------------
# # WEBHOOK
# # -------------------------
# @router.post("/webhook")
# async def webhook_handler(request: Request):
#     data = await request.json()

#     message_id = data.get("data", {}).get("id")
#     sender = data.get("data", {}).get("personEmail")

#     # Ignore bot's own messages
#     if sender == WEBEX_BOT_EMAIL:
#         return {"status": "ignored_bot"}

#     if not message_id:
#         return {"status": "ignored_no_message"}

#     msg = get_message(message_id)

#     text = msg.get("text", "").strip()
#     room_id = msg.get("roomId")

#     if not room_id or not text:
#         return {"status": "ignored_empty"}

#     # -------------------------
#     # INIT INTERVIEW
#     # -------------------------

#     # -------------------------
# # INIT INTERVIEW
# # -------------------------
#     state = ROOM_STATE[room_id]
#     if room_id not in ROOM_STATE:
#         ROOM_STATE[room_id] = {
#             "stage": STAGE_INTRO,
#             "last_question": FIRST_QUESTION,
#             "answers": [],
#             "technical_qna": [],
#             "tech_count": 0,
#             "hr_index": 0,
#             "profile": {},
#             "difficulty": "medium"   # 👈 important for adaptive logic
#         }

#         send_message(room_id, FIRST_QUESTION)
#         return {"status": "interview_started"}


#         # Store answer
#         state["answers"].append({
#             "question": state["last_question"],
#             "answer": text
#         })

#     # -------------------------
#     # INTRO → TECH
#     # -------------------------
#     # if state["stage"] == STAGE_INTRO:
#     #     next_question = "Can you explain your current role and key responsibilities?"
#     #     state["stage"] = STAGE_TECH
#     #     state["last_question"] = next_question
#     #     send_message(room_id, next_question)
#     #     return {"status": "tech_started"}

#     if state["stage"] == STAGE_INTRO:
#         state["stage"] = STAGE_TECH

#         # Simple adaptive rule (POC)
#         last_answer = text.lower()

#         if len(last_answer) > 120:
#             state["difficulty"] = "hard"
#         elif len(last_answer) < 40:
#             state["difficulty"] = "easy"
#         else:
#             state["difficulty"] = "medium"

#         next_question = ask_next_technical_question(
#             conversation=state["technical_qna"],
#             job_description=JOB_DESCRIPTION,
#             difficulty=state["difficulty"]
#         )

#         state["technical_qna"].append({
#             "question": next_question,
#             "answer": ""
#         })

#         state["tech_count"] = 1
#         state["last_question"] = next_question

#         send_message(room_id, next_question)
#         return {"status": "tech_started"}


#     # -------------------------
#     # TECH → HR (POC: single tech question)
#     # -------------------------
#     # if state["stage"] == STAGE_TECH:
#     #     state["stage"] = STAGE_HR
#     #     state["hr_index"] = 0
#     #     next_question = HR_QUESTIONS[0]
#     #     state["last_question"] = next_question
#     #     send_message(room_id, next_question)
#     #     return {"status": "hr_started"}

#     # -------------------------
#     # TECH QUESTIONS (5 max)
#     # -------------------------
#     if state["stage"] == STAGE_TECH:

#         # Store answer to last technical question
#         if state["technical_qna"]:
#             state["technical_qna"][-1]["answer"] = text

#         # Stop after 5 technical questions
#         if state["tech_count"] >= 5:
#             state["stage"] = STAGE_HR
#             state["hr_index"] = 0
#             next_q = HR_QUESTIONS[0]
#             state["last_question"] = next_q
#             send_message(room_id, next_q)
#             return {"status": "hr_started"}

#         # Ask next technical question
#         next_question = ask_next_technical_question(
#             conversation=state["technical_qna"],
#             job_description=JOB_DESCRIPTION
#         )

#         state["technical_qna"].append({
#             "question": next_question,
#             "answer": ""
#         })

#         state["tech_count"] += 1
#         state["last_question"] = next_question

#         send_message(room_id, next_question)
#         return {"status": "tech_continue"}


#     # -------------------------
#     # HR QUESTIONS
#     # -------------------------
#     if state["stage"] == STAGE_HR:

#         idx = state["hr_index"]

#         # Safety check
#         if idx < len(HR_QUESTIONS):
#             state["profile"][HR_QUESTIONS[idx]] = text
#             state["hr_index"] += 1

#         if state["hr_index"] < len(HR_QUESTIONS):
#             next_q = HR_QUESTIONS[state["hr_index"]]
#             state["last_question"] = next_q
#             send_message(room_id, next_q)
#             return {"status": "hr_continue"}

#         # -------------------------
#         # INTERVIEW COMPLETE
#         # -------------------------
#         feedback = generate_feedback(state["answers"])

#         email_body = f"""
# AI INTERVIEW FEEDBACK

# Candidate Responses:
# --------------------
# {feedback}

# HR DETAILS:
# -----------
# Experience: {state['profile'].get(HR_QUESTIONS[0])}
# Current CTC: {state['profile'].get(HR_QUESTIONS[1])}
# Expected CTC: {state['profile'].get(HR_QUESTIONS[2])}
# Notice Period: {state['profile'].get(HR_QUESTIONS[3])}
# """.strip()

#         try:
#             # send_feedback_email(
#             #     subject="AI Interview Feedback",
#             #     body=email_body
#             # )
            
#             print("\n" + "=" * 60)
#             print("AI INTERVIEW FEEDBACK (POC CONSOLE OUTPUT)")
#             print("=" * 60)
#             print(feedback)
#             print("\nHR DETAILS:")
#             print("-" * 20)
#             print(f"Experience     : {state['profile'].get(HR_QUESTIONS[0])}")
#             print(f"Current CTC    : {state['profile'].get(HR_QUESTIONS[1])}")
#             print(f"Expected CTC   : {state['profile'].get(HR_QUESTIONS[2])}")
#             print(f"Notice Period  : {state['profile'].get(HR_QUESTIONS[3])}")
#             print("=" * 60 + "\n")


#         except Exception as e:
#             print("EMAIL FAILED:", str(e))


#         send_message(
#             room_id,
#             "✅ Thank you for your time.\n\nThe interview is now complete."
#         )

#         state["stage"] = STAGE_COMPLETED
#         return {"status": "interview_completed"}

#     return {"status": "ok"}


import os
import requests
from fastapi import APIRouter, Request
from src.agent import generate_feedback
from src.agents import ask_next_technical_question

router = APIRouter()

# -------------------------
# ENV
# -------------------------
WEBEX_TOKEN = os.getenv("WEBEX_BOT_TOKEN")
WEBEX_BOT_EMAIL = os.getenv("WEBEX_BOT_EMAIL")

JOB_DESCRIPTION = """
Role: Senior RPA Developer

Required Skills:
- Blue Prism
- Python
- REST APIs
- Automation best practices
- Exception handling
- Orchestration and queues

Responsibilities:
- Design and develop enterprise-grade RPA solutions
- Handle production issues
- Work with business stakeholders
"""

API_BASE = "https://webexapis.com/v1"

headers = {
    "Authorization": f"Bearer {WEBEX_TOKEN}",
    "Content-Type": "application/json"
}

# -------------------------
# CONSTANTS
# -------------------------
STAGE_INTRO = "INTRO"
STAGE_TECH = "TECH"
STAGE_HR = "HR"
STAGE_COMPLETED = "COMPLETED"

FIRST_QUESTION = (
    "👋 Hi! Welcome to the AI Interview.\n\n"
    "Let’s begin.\n\n"
    "Tell me about yourself."
)

HR_QUESTIONS = [
    "How many years of total professional experience do you have?",
    "What is your current CTC (annual)?",
    "What is your expected CTC?",
    "What is your notice period (in days)?"
]

# -------------------------
# IN-MEMORY STATE (POC)
# -------------------------
ROOM_STATE = {}

# -------------------------
# WEBEX HELPERS
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
# WEBHOOK
# -------------------------
@router.post("/webhook")
async def webhook_handler(request: Request):
    data = await request.json()

    message_id = data.get("data", {}).get("id")
    sender = data.get("data", {}).get("personEmail")

    if sender == WEBEX_BOT_EMAIL or not message_id:
        return {"status": "ignored"}

    msg = get_message(message_id)
    text = msg.get("text", "").strip()
    room_id = msg.get("roomId")

    if not room_id or not text:
        return {"status": "ignored_empty"}

    # -------------------------
    # INIT INTERVIEW
    # -------------------------
    if room_id not in ROOM_STATE:
        ROOM_STATE[room_id] = {
            "stage": STAGE_INTRO,
            "last_question": FIRST_QUESTION,
            "answers": [],
            "technical_qna": [],
            "tech_count": 0,
            "hr_index": 0,
            "profile": {},
            "difficulty": "medium"
        }
        send_message(room_id, FIRST_QUESTION)
        return {"status": "interview_started"}

    state = ROOM_STATE[room_id]

    # -------------------------
    # STORE ANSWER
    # -------------------------
    state["answers"].append({
        "question": state["last_question"],
        "answer": text
    })

    # -------------------------
    # INTRO → TECH
    # -------------------------
    if state["stage"] == STAGE_INTRO:
        state["stage"] = STAGE_TECH

        if len(text) > 120:
            state["difficulty"] = "hard"
        elif len(text) < 40:
            state["difficulty"] = "easy"
        else:
            state["difficulty"] = "medium"

        next_question = ask_next_technical_question(
            conversation=[],
            job_description=JOB_DESCRIPTION,
            difficulty=state["difficulty"]
        )

        state["technical_qna"].append({
            "question": next_question,
            "answer": ""
        })

        state["tech_count"] = 1
        state["last_question"] = next_question

        send_message(room_id, next_question)
        return {"status": "tech_started"}

    # -------------------------
    # TECH QUESTIONS (MAX 5)
    # -------------------------
    if state["stage"] == STAGE_TECH:

        state["technical_qna"][-1]["answer"] = text

        # Adaptive difficulty
        if len(text) > 120:
            state["difficulty"] = "hard"
        elif len(text) < 40:
            state["difficulty"] = "easy"
        else:
            state["difficulty"] = "medium"

        if state["tech_count"] >= 5:
            state["stage"] = STAGE_HR
            state["hr_index"] = 0
            next_q = HR_QUESTIONS[0]
            state["last_question"] = next_q
            send_message(room_id, next_q)
            return {"status": "hr_started"}

        next_question = ask_next_technical_question(
            conversation=state["technical_qna"],
            job_description=JOB_DESCRIPTION,
            difficulty=state["difficulty"]
        )

        state["technical_qna"].append({
            "question": next_question,
            "answer": ""
        })

        state["tech_count"] += 1
        state["last_question"] = next_question

        send_message(room_id, next_question)
        return {"status": "tech_continue"}

    # -------------------------
    # HR QUESTIONS
    # -------------------------
    if state["stage"] == STAGE_HR:

        idx = state["hr_index"]
        state["profile"][HR_QUESTIONS[idx]] = text
        state["hr_index"] += 1

        if state["hr_index"] < len(HR_QUESTIONS):
            next_q = HR_QUESTIONS[state["hr_index"]]
            state["last_question"] = next_q
            send_message(room_id, next_q)
            return {"status": "hr_continue"}

        # -------------------------
        # INTERVIEW COMPLETE
        # -------------------------
        feedback = generate_feedback(state["answers"])

        print("\n" + "=" * 60)
        print("AI INTERVIEW FEEDBACK (POC CONSOLE OUTPUT)")
        print("=" * 60)
        print(feedback)
        print("\nHR DETAILS:")
        print("-" * 20)
        for q in HR_QUESTIONS:
            print(f"{q}: {state['profile'].get(q)}")
        print("=" * 60 + "\n")

        send_message(
            room_id,
            "✅ Thank you for your time.\n\nThe interview is now complete."
        )

        state["stage"] = STAGE_COMPLETED
        return {"status": "interview_completed"}

    return {"status": "ok"}

