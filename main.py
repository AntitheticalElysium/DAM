from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="Text Summarization API")

summarizer = pipeline("summarization", model="t5-small")

class TextInput(BaseModel):
    text: str

@app.post("/summarize")
def summarize(input: TextInput):
    summary = summarizer(input.text, max_length=60, min_length=15, do_sample=False)
    return {"summary": summary[0]['summary_text']}

