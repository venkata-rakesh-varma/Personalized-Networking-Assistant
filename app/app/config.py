import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

MODEL_NAMES = {
    "chat_model": "openai/gpt-oss-20b"
}

FACT_CHECK_API = "https://en.wikipedia.org/api/rest_v1/page/summary"