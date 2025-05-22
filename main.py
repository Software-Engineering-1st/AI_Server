from typing import List

from dotenv import load_dotenv
from openai import OpenAI
import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

with open("prompt.txt", "r", encoding="utf-8") as f:
    prompt = f.read()

class UserRequest(BaseModel):
    word: str
    meaning: List[str]

class AnswerResponse(BaseModel):
    answer: str

@app.post("/chat", response_model=AnswerResponse)
async def chat(request: UserRequest):
    try:
        user_input = (
                f"단어: {request.word}\n"
                f"뜻:\n" + "\n".join([f"- {m}" for m in request.meaning])
        )

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "developer", "content": prompt},
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
        )

        print(completion.choices[0].message.content)
        answer = completion.choices[0].message.content
        return {"answer": answer}

    except Exception as e:
        return {"answer": f"오류 발생: {str(e)}"}