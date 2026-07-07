import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import json

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="SmartBridge AI",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_URL = "https://personalized-networking-assistant-8afm.onrender.com"

# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "generated" not in st.session_state:
    st.session_state.generated = False

if "topics" not in st.session_state:
    st.session_state.topics = []

if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------------------------------
# Custom CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main{
    background:#0f172a;
}

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

/* Header */

.title{
    font-size:42px;
    font-weight:800;
    color:white;
}

.subtitle{
    font-size:18px;
    color:#cbd5e1;
}

/* Cards */

.metric-card{

    background:#1e293b;

    border-radius:18px;

    padding:18px;

    box-shadow:0px 0px 15px rgba(0,0,0,.25);

    text-align:center;

}

.theme-card{

    background:#2563eb;

    color:white;

    padding:10px 18px;

    border-radius:25px;

    display:inline-block;

    margin:5px;

    font-weight:bold;

}

.suggestion-card{

    background:#1e293b;

    padding:20px;

    border-radius:20px;

    border-left:7px solid #2563eb;

    margin-bottom:15px;

}

.history-card{

    background:#111827;

    padding:15px;

    border-radius:15px;

    margin-bottom:12px;

}

.stButton>button{

    background:#2563eb;

    color:white;

    border:none;

    border-radius:12px;

    height:50px;

    width:100%;

    font-size:16px;

    font-weight:bold;

}

.stButton>button:hover{

    background:#1d4ed8;

}

hr{
    border:1px solid #334155;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:

    st.image(
        "https://img.icons8.com/fluency/96/handshake.png",
        width=80
    )

    st.title("SmartBridge AI")

    st.caption("Personalized Networking Assistant")

    st.divider()

    page = st.radio(

        "Navigation",

        [

            "🏠 Dashboard",

            "🤖 Conversation Generator",

            "📜 History",

            "🔍 Fact Checker",

            "ℹ About"

        ]

    )

    st.divider()

    st.write("### AI Backend")

    st.success("Hugging Face GPT-OSS")

    st.write("### FastAPI")

    st.success("Connected")

    st.write("### Version")

    st.info("v2.0")

# ---------------------------------------------------
# Helper Functions
# ---------------------------------------------------

def load_history():

    try:

        response = requests.get(
            f"{BASE_URL}/history"
        )

        if response.status_code == 200:

            return response.json()

    except:

        pass

    return []


def submit_feedback(suggestion, feedback):

    requests.post(

        f"{BASE_URL}/feedback",

        json={

            "suggestion":suggestion,

            "feedback":feedback

        }

    )


def clear_history():

    requests.delete(

        f"{BASE_URL}/history"

    )


# ---------------------------------------------------
# Dashboard
# ---------------------------------------------------

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="title">🤝 SmartBridge AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">AI Powered Personalized Networking Assistant</div>',
        unsafe_allow_html=True
    )

    st.write("")

    history = load_history()

    total_events = len(history)

    total_topics = sum(
        len(item.get("topics", []))
        for item in history
    ) if history else 0

    total_suggestions = sum(
        len(item.get("suggestions", []))
        for item in history
    ) if history else 0

    c1,c2,c3 = st.columns(3)

    with c1:
        st.metric(
            "Events",
            total_events
        )

    with c2:
        st.metric(
            "Themes",
            total_topics
        )

    with c3:
        st.metric(
            "Conversation Starters",
            total_suggestions
        )

    st.divider()

    st.info(
        "👈 Use the sidebar to generate AI-powered networking conversation starters, review history, verify facts, and provide feedback."
    )
# =====================================================
# Conversation Generator
# =====================================================

elif page == "🤖 Conversation Generator":

    st.title("🤖 AI Conversation Generator")
    st.caption("Generate personalized networking conversation starters using AI.")

    col1, col2 = st.columns([2, 1])

    with col1:

        description = st.text_area(
            "📝 Event Description",
            placeholder="Example: An AI conference focusing on Generative AI, LLMs, Cloud Computing and Startups...",
            height=180,
        )

    with col2:

        interests = st.multiselect(
            "🎯 Your Interests",
            [
                "Artificial Intelligence",
                "Machine Learning",
                "Deep Learning",
                "Generative AI",
                "Python",
                "Java",
                "Cloud Computing",
                "Cybersecurity",
                "Blockchain",
                "Data Science",
                "Startups",
                "Entrepreneurship",
                "Software Development",
                "Web Development",
                "Mobile Development",
                "DevOps",
                "Networking",
                "Finance",
                "Healthcare",
                "Education"
            ]
        )

        st.info(
            "Choose your interests to make conversation starters more personalized."
        )

    st.write("")

    generate = st.button(
        "🚀 Generate Smart Conversation Starters",
        use_container_width=True
    )

    if generate:

        if description.strip() == "":
            st.warning("Please enter an event description.")
            st.stop()

        if len(interests) == 0:
            st.warning("Please select at least one interest.")
            st.stop()

        with st.spinner("🤖 AI is analyzing the event..."):

            try:

                response = requests.post(

                    f"{BASE_URL}/generate-conversation",

                    json={

                        "description": description,

                        "interests": interests

                    }

                )

                if response.status_code == 200:

                    data = response.json()

                    st.session_state.generated = True
                    st.session_state.topics = data["topics"]
                    st.session_state.suggestions = data["suggestions"]

                else:

                    st.error("Backend returned an error.")

            except Exception as e:

                st.error(str(e))

    # -------------------------------------
    # Display Results
    # -------------------------------------

    if st.session_state.generated:

        st.success("Conversation starters generated successfully!")

        st.write("")
        st.subheader("🏷 Detected Event Themes")

        cols = st.columns(len(st.session_state.topics))

        for i, topic in enumerate(st.session_state.topics):

            with cols[i]:

                st.markdown(
                    f"""
                    <div class="theme-card">
                    {topic}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.write("")
        st.subheader("💬 AI Conversation Starters")

        for index, suggestion in enumerate(st.session_state.suggestions):

            st.markdown(
                f"""
                <div class="suggestion-card">

                <h4>Conversation Starter {index+1}</h4>

                <p style="font-size:18px;">
                {suggestion}
                </p>

                </div>
                """,
                unsafe_allow_html=True,
            )

            c1, c2 = st.columns(2)

            with c1:

                if st.button(
                    f"👍 Helpful {index}",
                    use_container_width=True
                ):

                    submit_feedback(
                        suggestion,
                        "positive"
                    )

                    st.success("Feedback submitted!")

            with c2:

                if st.button(
                    f"👎 Not Helpful {index}",
                    use_container_width=True
                ):

                    submit_feedback(
                        suggestion,
                        "negative"
                    )

                    st.info("Feedback submitted!")

        st.write("")

        report = f"""
SMARTBRIDGE AI REPORT

Generated On:
{datetime.now()}

------------------------------------------------

Event Description

{description}

------------------------------------------------

Detected Themes

{chr(10).join(st.session_state.topics)}

------------------------------------------------

Conversation Starters

"""

        for i, s in enumerate(st.session_state.suggestions):

            report += f"\n{i+1}. {s}\n"

        st.download_button(

            "📥 Download Report",

            report,

            file_name="networking_report.txt",

            mime="text/plain",

            use_container_width=True

        )

        st.balloons()
# =====================================================
# HISTORY PAGE
# =====================================================

elif page == "📜 History":

    st.title("📜 Conversation History")
    st.caption("View all previously generated networking conversations.")

    history = load_history()

    if not history:
        st.info("No history available yet.")

    else:

        st.success(f"Total Sessions: {len(history)}")

        for index, item in enumerate(reversed(history)):

            with st.expander(f"Conversation #{len(history)-index}"):

                st.markdown("### 📝 Event Description")
                st.write(item["description"])

                st.markdown("### 🎯 Interests")
                st.write(", ".join(item["interests"]))

                st.markdown("### 🏷 Topics")

                cols = st.columns(len(item["topics"]))

                for i, topic in enumerate(item["topics"]):
                    with cols[i]:
                        st.markdown(
                            f"""
                            <div class="theme-card">
                            {topic}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                st.markdown("### 💬 Conversation Starters")

                for suggestion in item["suggestions"]:

                    st.markdown(
                        f"""
                        <div class="suggestion-card">
                        {suggestion}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    st.divider()

    if st.button(
        "🗑 Clear Conversation History",
        use_container_width=True,
    ):

        clear_history()

        st.success("History Cleared Successfully.")

        st.rerun()


# =====================================================
# FACT CHECKER
# =====================================================

elif page == "🔍 Fact Checker":

    st.title("🔍 AI Fact Checker")

    st.caption(
        "Verify concepts instantly using Wikipedia."
    )

    query = st.text_input(
        "Enter Topic",
        placeholder="Artificial Intelligence"
    )

    if st.button(
        "🔎 Verify",
        use_container_width=True
    ):

        if query.strip() == "":
            st.warning("Please enter a topic.")
        else:

            with st.spinner("Searching Wikipedia..."):

                try:

                    response = requests.post(

                        f"{BASE_URL}/fact-check",

                        json={

                            "query": query

                        }

                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.success("Verified Successfully")

                        st.markdown("### 📚 Summary")

                        st.write(data["summary"])

                    else:

                        st.error("Unable to verify topic.")

                except Exception as e:

                    st.error(str(e))


# =====================================================
# ABOUT PAGE
# =====================================================

elif page == "ℹ About":

    st.title("🤝 SmartBridge AI")

    st.markdown(
        """
## Personalized Networking Assistant

SmartBridge AI helps users generate personalized
networking conversation starters using Artificial Intelligence.

---

### 🚀 Features

✅ Event Theme Detection

✅ AI Conversation Generation

✅ Conversation History

✅ Feedback Collection

✅ Fact Checker

✅ Download Report

---

### 🛠 Tech Stack

- FastAPI
- Streamlit
- Hugging Face
- Python
- REST API

---

### 👨‍💻 Developed By

Computer Science Engineering Student

SmartBridge Internship Project
"""
    )

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Backend",
            "FastAPI"
        )

    with c2:
        st.metric(
            "AI",
            "Hugging Face"
        )

    with c3:
        st.metric(
            "Frontend",
            "Streamlit"
        )

    st.divider()

    st.success(
        "Thank you for using SmartBridge AI!"
    )