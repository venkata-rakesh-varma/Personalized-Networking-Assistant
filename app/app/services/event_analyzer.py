import json
from huggingface_hub import InferenceClient
from app.config import HF_API_KEY, MODEL_NAMES

client = InferenceClient(api_key=HF_API_KEY)


def extract_event_themes(description):

    prompt = f"""
Extract ONLY the three most relevant themes.

Event:

{description}

Return ONLY JSON.

Example:

["AI","Healthcare","Networking"]
"""

    try:

        response = client.chat.completions.create(
            model=MODEL_NAMES["chat_model"],
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        answer = response.choices[0].message.content.strip()

        return json.loads(answer)

    except Exception as e:

        print(e)

    return [
        "Technology",
        "Networking",
        "Professional Development"
    ]