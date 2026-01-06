# src/main.py
import os
import json
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv

load_dotenv()

#from routers.webex_bot import get_message, send_message
#from routers.webex_bot import router as webex_router
from src.routers.webex_bot import router as webex_router

from src.agent import evaluate_and_next

app = FastAPI()
app.include_router(webex_router)


BOT_EMAIL = os.getenv("WEBEX_BOT_EMAIL")

@app.get("/")
def home():
    return {"message": "Webex AI Interviewer POC is running!"}

# @app.post("/webhook/webex")
# async def webex_webhook(req: Request):
#     """
#     Webex will POST here on events like messages.created
#     We'll:
#      1. fetch full message (via Webex REST using id)
#      2. ignore our own messages
#      3. call agent to evaluate and get next question
#      4. reply into the same room
#     """
#     payload = await req.json()
#     # payload structure: { "id": "...", "resource": "messages", "event": "created", "data": {"id": "..."} }
#     try:
#         resource = payload.get("resource")
#         event = payload.get("event")
#         data = payload.get("data", {})
#         if resource != "messages" or event != "created":
#             return {"status": "ignored"}
#         message_id = data.get("id")
#         if not message_id:
#             return {"status": "no_message_id"}
#         # fetch full message
#         msg = get_message(message_id)
#         text = msg.get("text", "")
#         person_email = msg.get("personEmail")
#         room_id = msg.get("roomId")
#         # ignore messages from the bot itself
#         if person_email == BOT_EMAIL:
#             return {"status": "ignored_self"}
#         # For a simple workflow: we assume the candidate answers a previous question.
#         # We'll pass question_text placeholder (in later steps we'll store last question per room).
#         question_text = "Previous question (placeholder)."
#         model_text = evaluate_and_next(question_text=question_text, answer_text=text)
#         # Here we simply send model_text back to room for now
#         send_message(room_id, model_text)
#         return {"status": "ok"}
#     except Exception as e:
#         # log error (avoid crashing)
#         raise HTTPException(status_code=500, detail=str(e))
