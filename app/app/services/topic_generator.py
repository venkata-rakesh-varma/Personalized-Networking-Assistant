from huggingface_hub import InferenceClient
from app.config import HF_API_KEY, MODEL_NAMES

client = InferenceClient(api_key=HF_API_KEY)


def generate_topics(event_themes, user_interests):

    prompt = f"""
You are a networking coach.

Event themes:

{', '.join(event_themes)}

User interests:

{', '.join(user_interests)}

Generate exactly three professional networking conversation starters.

Return only bullet points.
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
            temperature=0.7
        )

        text = response.choices[0].message.content

        suggestions = []

        for line in text.split("\n"):

            line = line.strip()

            if line.startswith("-"):
                suggestions.append(line[1:].strip())

            elif line[:2].isdigit():
                suggestions.append(line[2:].strip())

        return suggestions[:3]

    except Exception as e:

        print(e)

    return [
        "What inspired you to attend this event?",
        "What exciting projects are you currently working on?",
        "Which emerging technologies interest you the most?"
    ]