

# import os
# from openai import OpenAI

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# if not OPENAI_API_KEY:
#     raise RuntimeError("OPENAI_API_KEY environment variable not set")

# client = OpenAI(api_key=OPENAI_API_KEY)

# # SYSTEM_PROMPT = """
# # You are an AI technical interviewer.

# # Rules:
# # - Ask ONLY one interview question at a time
# # - Do NOT answer questions yourself
# # - Adapt the next question based on the candidate's answer
# # - Keep questions concise, professional, and relevant
# # - Do NOT include explanations or feedback unless explicitly asked
# # """
# # JOB_DESCRIPTION = """
# # •	5-7 years of hands-on experience in .NET development
# # •	Proficient in C# with a deep understanding of advanced concepts and features
# # •	Strong command of OOPS principles and implementation
# # •	Working knowledge of Git and SourceTree for source code management
# # •	Comprehensive understanding of design patterns, architectural patterns, and SOLID principles
# # •	Familiarity with Windows UI Graphical Framework and automation technologies
# # •	Working knowledge of Web API
# # •	Experience with database technologies such as SQL Server, Oracle, and MySQL"""

# JOB_DESCRIPTION = """
# Role: Python Backend Developer

# Requirements:
# - Strong experience in Python
# - Experience with FastAPI or Flask
# - REST API design and integration
# - Working knowledge of SQL databases
# - Understanding of async programming
# - Experience with cloud deployment (AWS/GCP/Azure preferred)
# """

# SYSTEM_PROMPT = """
# You are an AI Interview Agent conducting an initial screening interview for a job role.

# ROLE & BEHAVIOR:
# - You are conducting a structured screening interview.
# - Ask ONE question at a time.
# - Keep questions concise, professional, and relevant.
# - Adapt follow-up questions based on the candidate’s previous answers.
# - Do NOT provide answers or explanations.

# INTERVIEW STRUCTURE (STRICT):
# 1. Introduction (1 question only)
# 2. HR Screening Questions (fixed)
# 3. Technical Screening Questions (5–6 questions MAX)
# 4. End the interview politely after technical questions

# HR SCREENING QUESTIONS (ASK ONCE EACH):
# - Total years of experience
# - Current company and role
# - Current CTC
# - Expected CTC
# - Notice period (in days)
# - Reason for job change

# TECHNICAL SCREENING RULES:
# - Ask ONLY 5 to 6 technical questions.
# - Questions MUST be strictly based on the provided Job Description.
# - Do NOT ask anything outside the Job Description.
# - Increase difficulty gradually.
# - Focus on practical, real-world scenarios.
# - Avoid trivia or purely theoretical questions.

# JOB DESCRIPTION:
# {JOB_DESCRIPTION}

# IMPORTANT CONSTRAINTS:
# - Do NOT exceed 6 technical questions.
# - Do NOT repeat questions.
# - Do NOT mention selection or rejection.
# - After completing all questions, politely conclude the interview.
# """


# # def evaluate_and_next(last_question: str, answer_text: str) -> str:
# #     """
# #     Takes the last question and candidate answer
# #     Returns the next interview question only
# #     """

# #     response = client.chat.completions.create(
# #         model="gpt-4o-mini",
# #         messages=[
# #             {"role": "system", "content": SYSTEM_PROMPT},
# #             {
# #                 "role": "user",
# #                 "content": f"""
# # Last interview question:
# # {last_question}

# # Candidate answer:
# # {answer_text}

# # Ask the next interview question.
# # """
# #             }
# #         ],
# #         temperature=0.6,
# #         max_tokens=120
# #     )

# #     return response.choices[0].message.content.strip()

# def evaluate_and_next(last_question: str, answer_text: str, job_description: str) -> str:
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {
#                 "role": "system",
#                 "content": SYSTEM_PROMPT.format(
#                     JOB_DESCRIPTION=job_description
#                 )
#             },
#             {
#                 "role": "user",
#                 "content": f"""
# Last question:
# {last_question}

# Candidate answer:
# {answer_text}

# Ask the next appropriate interview question based on the interview structure.
# """
#             }
#         ],
#         temperature=0.6
#     )

#     return response.choices[0].message.content.strip()


# def generate_feedback(answers: list) -> str:
#     formatted = "\n".join(
#         f"Q: {a['question']}\nA: {a['answer']}" for a in answers
#     )

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {
#                 "role": "system",
#                 "content": (
#                     "You are an interview evaluator. "
#                     "Provide professional feedback on strengths, weaknesses, "
#                     "communication, and technical depth. "
#                     "DO NOT mention selection or rejection."
#                 )
#             },
#             {
#                 "role": "user",
#                 "content": formatted
#             }
#         ],
#         temperature=0.4
#     )

#     return response.choices[0].message.content.strip()

# # def ask_next_technical_question(conversation):
# #     """
# #     Uses existing SYSTEM_PROMPT + Job Description
# #     Asks the next technical interview question
# #     """

# #     messages = [
# #         {"role": "system", "content": SYSTEM_PROMPT}
# #     ]

# #     for qa in conversation:
# #         messages.append({"role": "user", "content": qa["question"]})
# #         messages.append({"role": "assistant", "content": qa["answer"]})

# #     messages.append({
# #         "role": "user",
# #         "content": "Ask the next technical interview question strictly based on the job description."
# #     })

# #     response = client.chat.completions.create(
# #         model="gpt-4o-mini",
# #         messages=messages,
# #         temperature=0.3
# #     )

# #     return response.choices[0].message.content.strip()

# def ask_next_technical_question(
#     conversation: list,
#     job_description: str,
#     difficulty: str
# ) -> str:

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {
#                 "role": "system",
#                 "content": f"""
# You are an AI technical interviewer.

# Rules:
# - Ask ONE technical question only
# - Difficulty: {difficulty}
# - No explanations
# - No feedback
# - Stick strictly to Job Description

# Job Description:
# {job_description}
# """
#             },
#             {
#                 "role": "user",
#                 "content": f"""
# Previous technical Q&A:
# {conversation}

# Ask the next question.
# """
#             }
#         ],
#         temperature=0.6
#     )

#     return response.choices[0].message.content.strip()


# def evaluate_technical_answer(
#     question: str,
#     answer: str,
#     job_description: str
# ) -> dict:
#     """
#     Evaluates candidate answer and returns:
#     - score (0–10)
#     - difficulty_adjustment: up | same | down
#     """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {
#                 "role": "system",
#                 "content": f"""
# You are a technical interviewer.
# Evaluate the candidate answer strictly based on this Job Description:

# {job_description}

# Return output ONLY in JSON.
# """
#             },
#             {
#                 "role": "user",
#                 "content": f"""
# Question:
# {question}

# Candidate Answer:
# {answer}

# Evaluate the answer.
# """
#             }
#         ],
#         temperature=0.2
#     )

#     return json.loads(response.choices[0].message.content)


import os
import json
from openai import OpenAI

# -------------------------
# OPENAI CLIENT
# -------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")

client = OpenAI(api_key=OPENAI_API_KEY)

# -------------------------
# SYSTEM PROMPT TEMPLATE
# -------------------------
SYSTEM_PROMPT = """
You are an AI Interview Agent conducting an initial screening interview for a job role.

ROLE & BEHAVIOR:
- You are conducting a structured screening interview.
- Ask ONE question at a time.
- Keep questions concise, professional, and relevant.
- Adapt follow-up questions based on the candidate’s previous answers.
- Do NOT provide answers or explanations.

INTERVIEW STRUCTURE (STRICT):
1. Introduction (1 question only)
2. HR Screening Questions (fixed)
3. Technical Screening Questions (5–6 questions MAX)
4. End the interview politely after technical questions

HR SCREENING QUESTIONS (ASK ONCE EACH):
- Total years of experience
- Current company and role
- Current CTC
- Expected CTC
- Notice period (in days)
- Reason for job change

TECHNICAL SCREENING RULES:
- Ask ONLY 5 to 6 technical questions.
- Questions MUST be strictly based on the provided Job Description.
- Do NOT ask anything outside the Job Description.
- Increase difficulty gradually.
- Focus on practical, real-world scenarios.
- Avoid trivia or purely theoretical questions.

JOB DESCRIPTION:
{JOB_DESCRIPTION}

IMPORTANT CONSTRAINTS:
- Do NOT exceed 6 technical questions.
- Do NOT repeat questions.
- Do NOT mention selection or rejection.
- After completing all questions, politely conclude the interview.
"""

# -------------------------
# NEXT INTERVIEW QUESTION
# -------------------------
def evaluate_and_next(last_question: str, answer_text: str, job_description: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT.format(JOB_DESCRIPTION=job_description)
            },
            {
                "role": "user",
                "content": f"""
Last question:
{last_question}

Candidate answer:
{answer_text}

Ask the next appropriate interview question based on the interview structure.
"""
            }
        ],
        temperature=0.6
    )
    return response.choices[0].message.content.strip()

# -------------------------
# GENERATE FEEDBACK
# -------------------------
def generate_feedback(answers: list) -> str:
    formatted = "\n".join(
        f"Q: {a['question']}\nA: {a['answer']}" for a in answers
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an interview evaluator. "
                    "Provide professional feedback on strengths, weaknesses, "
                    "communication, and technical depth. "
                    "DO NOT mention selection or rejection."
                )
            },
            {"role": "user", "content": formatted}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content.strip()

# -------------------------
# NEXT TECH QUESTION (ADAPTIVE)
# -------------------------
def ask_next_technical_question(conversation: list, job_description: str, difficulty: str) -> str:
    """
    Returns the next technical question based on previous Q&A,
    Job Description, and adaptive difficulty.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
You are an AI technical interviewer.

Rules:
- Ask ONE technical question only
- Difficulty: {difficulty}
- No explanations
- No feedback
- Stick strictly to Job Description

Job Description:
{job_description}
"""
            },
            {
                "role": "user",
                "content": f"Previous technical Q&A:\n{conversation}\n\nAsk the next question."
            }
        ],
        temperature=0.6
    )
    return response.choices[0].message.content.strip()

# -------------------------
# EVALUATE TECHNICAL ANSWER
# -------------------------
def evaluate_technical_answer(question: str, answer: str, job_description: str) -> dict:
    """
    Evaluates candidate answer and returns:
    - score (0–10)
    - difficulty_adjustment: up | same | down
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
You are a technical interviewer.
Evaluate the candidate answer strictly based on this Job Description:

{job_description}

Return output ONLY in JSON:
- score (0-10)
- difficulty_adjustment: up | same | down
"""
            },
            {
                "role": "user",
                "content": f"""
Question:
{question}

Candidate Answer:
{answer}

Provide JSON output only.
"""
            }
        ],
        temperature=0.2
    )
    return json.loads(response.choices[0].message.content)
