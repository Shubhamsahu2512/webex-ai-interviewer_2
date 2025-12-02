from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Webex AI Interviewer POC is running!"}
