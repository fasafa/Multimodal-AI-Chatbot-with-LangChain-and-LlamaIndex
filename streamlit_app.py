import streamlit as st
import requests
from PIL import Image
import io

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(
    page_title="Multimodal AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Apply some modern CSS
st.markdown("""
    <style>
        body {
            background-color: #f7f9fc;
        }
        .chat-box {
            background-color: #ffffff;
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
        }
        .user-bubble {
            background-color: #DCF8C6;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
        }
        .bot-bubble {
            background-color: #F1F0F0;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# BACKEND URL (your Flask server)
# -------------------------------
BACKEND_URL = "http://127.0.0.1:8080"

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("🧠 Multimodal AI Chatbot")
st.sidebar.info(
    "Ask me questions or upload an image for analysis.\n\n"
    "This app uses local models — Qwen for text and BLIP for image understanding."
)
mode = st.sidebar.radio("Choose mode:", ["💬 Text Chat", " Image Query"])

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# TEXT CHAT MODE
# -------------------------------
if mode == "💬 Text Chat":
    st.title("💬 Chat with AI")

    # Chat history
    for msg in st.session_state.messages:
        role, content = msg["role"], msg["content"]
        if role == "user":
            st.markdown(f"<div class='user-bubble'><b>You:</b> {content}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-bubble'><b>AI:</b> {content}</div>", unsafe_allow_html=True)

    # User input
    user_input = st.text_input("Enter your question:")
    if st.button("Ask"):
        if user_input.strip() != "":
            with st.spinner("Thinking..."):
                response = requests.post(f"{BACKEND_URL}/query/text", json={"query": user_input})
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No response from model.")
                else:
                    answer = f"Error: {response.text}"

            # Update session history
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "bot", "content": answer})
            st.rerun()

# -------------------------------
# IMAGE QUERY MODE
# -------------------------------
else:
    st.title("🖼️ Ask About an Image")

    uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])
    question = st.text_input("Ask a question about the image:", value="Describe this image.")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        if st.button("Analyze Image"):
            with st.spinner("Analyzing image..."):
                files = {"image": uploaded_file.getvalue()}
                data = {"question": question}
                response = requests.post(f"{BACKEND_URL}/query/image", files=files, data=data)

                if response.status_code == 200:
                    result = response.json()
                    answer = result.get("answer", "No response.")
                else:
                    answer = f"Error: {response.text}"

            st.markdown(f"<div class='bot-bubble'><b>AI:</b> {answer}</div>", unsafe_allow_html=True)

