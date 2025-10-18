# streamlit_app.py
import streamlit as st
import requests
from PIL import Image
import io
import os

API_BASE = os.environ.get("API_BASE", "http://localhost:8080")

st.title("Multimodal Q&A (LangChain + LlamaIndex)")

mode = st.radio("Mode", ["Text", "Image"])

if mode == "Text":
    q = st.text_area("Question", height=120)
    if st.button("Ask"):
        r = requests.post(f"{API_BASE}/query/text", json={"query": q})
        if r.ok:
            st.write("**Answer:**")
            st.write(r.json())
        else:
            st.error(f"Error: {r.text}")

else:
    uploaded_file = st.file_uploader("Upload an image", type=["png","jpg","jpeg"])
    question = st.text_input("Question about the image", value="Describe the image")
    if uploaded_file and st.button("Ask about image"):
        files = {"image": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        data = {"question": question}
        r = requests.post(f"{API_BASE}/query/image", files=files, data=data)
        if r.ok:
            st.write("**Answer:**")
            st.json(r.json())
        else:
            st.error(f"Error: {r.text}")
