from dotenv import load_dotenv
import google.generativeai as genai

# load all env variables
load_dotenv()
import os

# setup gemini ai instance
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')