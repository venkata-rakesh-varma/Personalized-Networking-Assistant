# app/routers/conversation.py

from fastapi import APIRouter
from pathlib import Path
import json

from app.models.schemas import (
    EventInput,
    ConversationRequest,
    FactCheckRequest,
    ConversationResponse,
    FactCheckResponse,
)

from app.services import (
    event_analyzer,
    topic_generator,
    fact_checker,
    history_logger,
    feedback_logger,
)

router = APIRouter()


# -------------------------------------------------------
# Analyze Event Themes
# -------------------------------------------------------
@router.post("/analyze-event")
def analyze_event(data: EventInput):
    themes = event_analyzer.extract_event_themes(data.description)
    return {"topics": themes}


# -------------------------------------------------------
# Fact Checker
# -------------------------------------------------------
@router.post("/fact-check", response_model=FactCheckResponse)
def fact_check(data: FactCheckRequest):
    summary = fact_checker.fact_check(data.query)
    return FactCheckResponse(summary=summary)


# -------------------------------------------------------
# Generate Conversation Starters
# -------------------------------------------------------
@router.post("/generate-conversation", response_model=ConversationResponse)
def generate_conversation(data: ConversationRequest):

    themes = event_analyzer.extract_event_themes(data.description)

    suggestions = topic_generator.generate_topics(
        themes,
        data.interests
    )

    # Save conversation history
    history_logger.log_conversation({
        "description": data.description,
        "interests": data.interests,
        "topics": themes,
        "suggestions": suggestions
    })

    return ConversationResponse(
        topics=themes,
        suggestions=suggestions
    )


# -------------------------------------------------------
# Get Conversation History
# -------------------------------------------------------
@router.get("/history")
def get_history():
    return history_logger.load_history()


# -------------------------------------------------------
# Submit Feedback
# -------------------------------------------------------
@router.post("/feedback")
def submit_feedback(data: dict):

    feedback_logger.log_feedback(
        suggestion=data["suggestion"],
        action=data["feedback"]
    )

    return {
        "status": "success",
        "message": "Feedback saved successfully."
    }


# -------------------------------------------------------
# Get Feedback
# -------------------------------------------------------
@router.get("/feedback")
def get_feedback():
    return feedback_logger.get_feedback()


# -------------------------------------------------------
# Clear History
# -------------------------------------------------------
@router.delete("/history")
def clear_history():

    history_file = Path("history.json")

    with open(history_file, "w") as f:
        json.dump([], f, indent=2)

    return {
        "status": "success",
        "message": "Conversation history cleared."
    }


# -------------------------------------------------------
# Clear Feedback
# -------------------------------------------------------
@router.delete("/feedback")
def clear_feedback():

    feedback_file = Path("feedback.json")

    with open(feedback_file, "w") as f:
        json.dump([], f, indent=2)

    return {
        "status": "success",
        "message": "Feedback history cleared."
    }