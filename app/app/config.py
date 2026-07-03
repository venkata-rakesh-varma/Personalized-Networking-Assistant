import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAMES = {
    "event_analysis": "valhalla/distilbart-mnli-12-3",
    "text_generator": "gpt2"
}

FACT_CHECK_API = "https://en.wikipedia.org/api/rest_v1/page/summary"
HF_API_KEY = os.getenv("HF_API_KEY")