import os
import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(

    
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
    }
    .main-header p {
        color: #e0e0e0;
        margin: 0.5rem 0 0 0;
    }

    /* Force ALL chat messages to have dark background */
    .stChatMessage,
    [data-testid="stChatMessage"],
    [class*="stChatMessage"] {
        background-color: #1e3a5f !important;
        border-radius: 15px !important;
        margin: 0.5rem 0 !important;
        padding: 1rem !important;
        border: 1px solid #3b82f6 !important;
    }

    /* Force ALL text inside chat to WHITE */
    .stChatMessage *,
    [data-testid="stChatMessage"] *,
    [class*="stChatMessage"] * {
        color: #ffffff !important;
    }

    /* Remove any white/light backgrounds inside messages */
    .stChatMessage div,
    .stChatMessage p,
    .stChatMessage span,
    [data-testid="stChatMessage"] div,
    [data-testid="stChatMessageContent"],
    [data-testid="stChatMessageContent"] div,
    [data-testid="stChatMessageContent"] p {
        background-color: transparent !important;
        background: transparent !important;
        color: #ffffff !important;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
    }
    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }

    /* Input box - BLACK text for typing */
    .stChatInput textarea {
        color: #000000 !important;
    }
    
    /* Metric value color fix */
    [data-testid="stMetricValue"] {
        color: #60a5fa !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Chatbot</h1>
    <p>Built by Zeeshan Ullah | Data Scientist & ML Engineer</p>
</div>
""", unsafe_allow_html=True)

# Initialize client
@st.cache_resource
def get_client():
    return InferenceClient(token=os.getenv("HUGGINGFACEHUB_API_TOKEN"))

client = get_client()
MODEL = "Qwen/Qwen2.5-72B-Instruct"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    max_tokens = st.slider("Max Response Length", 100, 1000, 500)
    
    st.markdown("---")
    st.markdown("### 📊 Chat Stats")
    st.metric("Messages", len(st.session_state.messages))
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### ℹ️ About This App")
    st.markdown("""
    **Tech Stack:**
    - **Model**: Qwen 2.5 72B
    - **Provider**: HuggingFace
    - **UI**: Streamlit
    """)

    st.markdown("---")
    st.markdown("### 👨‍💻 Developer")
    st.markdown("""
    **Zeeshan Ullah**
    *Data Scientist | ML Engineer | AI & NLP Enthusiast*

    **Skills:** Python, Machine Learning, NLP, SQL, Power BI, Azure

    **Education:**
    BS Computer Science
    Abdul Wali Khan University
    """)
    st.markdown("[LinkedIn](https://www.linkedin.com/in/zeeshanullah) | [GitHub](https://github.com/KhattakDataLab) | [Email](mailto:ullahzeeshan202@gmail.com)")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🧑" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            try:
                api_messages = [{"role": m["role"], "content": m["content"]} 
                               for m in st.session_state.messages]
                
                response = client.chat_completion(
                    model=MODEL,
                    messages=api_messages,
                    max_tokens=max_tokens
                )
                
                bot_response = response.choices[0].message.content
                st.markdown(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
