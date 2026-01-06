# # src/agent.py
# import os
# import openai

# openai.api_key = os.getenv("OPENAI_API_KEY")

# # small system prompt to instruct the model
# SYSTEM_PROMPT = """
# You are an interview assistant. Read the candidate's short answer and
# (1) give a short evaluation (1-5),
# (2) give a 1-2 sentence feedback,
# (3) propose the next question.
# Respond in JSON format like:
# {"score": 4, "feedback": "Good concise answer ...", "next_question": "Follow-up?"}
# """

# # def evaluate_and_next(question_text: str, answer_text: str):
# #     """
# #     Call OpenAI Chat Completion (simple) to evaluate the answer and produce the next question.
# #     """
# #     user_msg = f"Question: {question_text}\nAnswer: {answer_text}\nProvide score, feedback, and next question."
# #     response = openai.ChatCompletion.create(
# #         model="gpt-4o-mini",  # change if you prefer another model
# #         messages=[
# #             {"role": "system", "content": SYSTEM_PROMPT},
# #             {"role": "user", "content": user_msg}
# #         ],
# #         max_tokens=200,
# #         temperature=0.2,
# #     )
# #     # best-effort parse
# #     text = response["choices"][0]["message"]["content"].strip()
# #     return text

# def evaluate_and_next(question_text: str, answer_text: str):
#     user_msg = f"""
#     Question: {question_text}
#     Answer: {answer_text}

#     Evaluate the answer and respond strictly in JSON:
#     {{
#     "score": number (1-5),
#     "feedback": "short feedback",
#     "next_question": "next interview question"
#     }}
#     """

#     response = openai.ChatCompletion.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {"role": "user", "content": user_msg}
#         ],
#         max_tokens=200,
#         temperature=0.2,
#     )

#     text = response["choices"][0]["message"]["content"]

#     try:
#         return json.loads(text)
#     except Exception:
#         return {
#             "score": 3,
#             "feedback": "Answer received.",
#             "next_question": "Can you explain that in more detail?"
#         }


# src/agent.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an AI technical interviewer.
You ask one question at a time.
You adapt questions based on candidate answers.
Keep questions concise and professional.
"""

def evaluate_and_next(last_question: str, answer_text: str) -> str:
    """
    Takes the last question and candidate answer
    Returns the next interview question
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
Last question:
{last_question}

Candidate answer:
{answer_text}

Ask the next interview question.
"""
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
