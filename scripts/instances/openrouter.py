from openai import OpenAI
from dotenv import load_dotenv

# load all env variables
load_dotenv()
import os

# setup gemini ai instance
api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

async def response(prompt: str) -> str:
    completion = client.chat.completions.create(
        model="google/gemini-2.0-flash-001", # not free, but has limit
        messages=[
            {
            "role": "user",
            "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content