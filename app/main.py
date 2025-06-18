# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.model import get_answer_and_links

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None   # base64‐encoded screenshot

@app.post("/", response_model=dict)
async def answer_question(req: QuestionRequest):
    try:
        # you could decode/ocr req.image here, if desired
        return get_answer_and_links(req.question)
    except Exception as e:
        detail = str(e).lower()
        if "rate limit" in detail or "quota" in detail:
            raise HTTPException(503, "OpenAI rate limit exceeded or quota insufficient.")
        raise HTTPException(500, f"Internal server error: {e}")
