import streamlit as st
import requests

# --- Configuration ---
API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Networking Assistant",
    page_icon="🤝",
    layout="centered"
)

# --- Header ---
st.title("🤝 Personalized Networking Assistant")
st.markdown("Generate context-aware conversation starters and fact-check topics before your next event.")
st.divider()

# --- Application Tabs ---
tab1, tab2 = st.tabs(["💬 Generate Starters", "🔍 Fact Checker"])

# --- TAB 1: Generator Flow ---
with tab1:
    st.header("Icebreaker Generator")
    
    event_desc = st.text_area(
        "Event Description", 
        placeholder="e.g., A local tech meetup focused on the future of artificial intelligence in healthcare.", 
        height=120
    )
    
    user_interests = st.text_input(
        "Your Interests (comma-separated)", 
        placeholder="e.g., machine learning, cloud computing, startups"
    )

    if st.button("Generate Conversation Starters", type="primary"):
        if event_desc and user_interests:
            with st.spinner("Analyzing event and generating starters..."):
                # Clean up the comma-separated string into a list
                interests_list = [i.strip() for i in user_interests.split(",") if i.strip()]
                
                payload = {
                    "description": event_desc,
                    "interests": interests_list
                }
                
                try:
                    response = requests.post(f"{API_BASE_URL}/generate-conversation", json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Analysis Complete!")
                        
                        st.subheader("Detected Event Themes")
                        # Display themes horizontally using Streamlit columns
                        cols = st.columns(len(data.get("topics", [])))
                        for idx, topic in enumerate(data.get("topics", [])):
                            cols[idx].info(topic)
                        
                        st.subheader("Your Conversation Starters")
                        for suggestion in data.get("suggestions", []):
                            st.markdown(f"> **{suggestion}**")
                            
                    else:
                        st.error(f"Error from API: {response.status_code} - {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Failed to connect to the backend. Is your FastAPI server running on port 8000?")
        else:
            st.warning("Please provide both an event description and your interests.")

# --- TAB 2: Fact-Checking Flow ---
with tab2:
    st.header("Quick Fact Checker")
    st.markdown("Need to verify a concept before discussing it? Search Wikipedia below.")
    
    fact_query = st.text_input("Topic to verify:", placeholder="e.g., DistilBERT")
    
    if st.button("Check Fact"):
        if fact_query:
            with st.spinner("Searching..."):
                payload = {"query": fact_query}
                try:
                    response = requests.post(f"{API_BASE_URL}/fact-check", json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Result Found:")
                        st.write(data.get("summary", "No summary provided."))
                    else:
                        st.error("Failed to retrieve fact check.")
                except requests.exceptions.ConnectionError:
                    st.error("Failed to connect to the backend. Is your FastAPI server running?")
        else:
            st.warning("Please enter a topic to check.")