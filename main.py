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
    question: str

class AnswerResponse(BaseModel):
    answer: str

@app.post("/chat", response_model=AnswerResponse)
async def chat(request: UserRequest):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "developer", "content": prompt},
                {
                    "role": "user",
                    "content": request.question,
                },
            ],
        )

        print(completion.choices[0].message.content)
        answer = completion.choices[0].message.content
        return {"answer": answer}

    except Exception as e:
        return {"answer": f"오류 발생: {str(e)}"}