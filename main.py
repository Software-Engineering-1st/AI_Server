import openai
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()
openai.api_key = ""

with open("prompt.txt", "r", encoding="utf-8") as f:
    prompt = f.read()

class UserRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat(request: UserRequest):
    response = await openai.ChatCompletion.acreate(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": request.prompt}
        ]
    )
    return {"response": response.choices[0].message.content.strip()}