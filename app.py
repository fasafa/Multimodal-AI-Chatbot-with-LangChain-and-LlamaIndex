import os
import io
import json
import time
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
from PIL import Image

from llama_index.core import VectorStoreIndex, StorageContext, Document
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")



# Load environment variables from .env
# load_dotenv()

# # Access your OpenAI API key
# openai_api_key = os.getenv("OPENAI_API_KEY")

# if not openai_api_key:
#     raise ValueError("OpenAI API key not found. Please set it in your .env file.")

# # Set it for OpenAI usage
# os.environ["OPENAI_API_KEY"] = openai_api_key


HF_INFERENCE_API = os.environ.get("HF_INFERENCE_API")  # your Hugging Face Inference API token
INDEX_DIR = os.environ.get("INDEX_DIR", "index_store")

app = Flask(__name__)
# limiter = Limiter(app, key_func=get_remote_address, default_limits=["30/minute"])  # tune as needed
# initialize limiter (new way for v3+)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["30 per minute"],
)
limiter.init_app(app)

# Load persisted LlamaIndex
storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
# index = VectorStoreIndex.load_from_disk(INDEX_DIR) if os.path.exists(INDEX_DIR) else None
from llama_index.core import StorageContext, load_index_from_storage

if os.path.exists(INDEX_DIR):
    print("📂 Loading existing index from storage...")
    storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
    index = load_index_from_storage(storage_context)
else:
    print("⚠️ No existing index found. Please run llama_index_ingest.py first.")
    index = None


def call_hf_multimodal_model(image_bytes=None, prompt="Describe the image"):
    """
    Simple wrapper to call Hugging Face Inference API for a multimodal model.
    Many HF models accept image + text in the request; consult model docs.
    """
    headers = {"Authorization": f"Bearer {HF_INFERENCE_API}"}
    # Example: some HF image+text endpoints accept multipart form
    files = {}
    data = {"inputs": prompt}
    if image_bytes:
        files["image"] = ("image.jpg", image_bytes, "image/jpeg")
    resp = requests.post(
        "https://api-inference.huggingface.co/models/qwen-local",
        headers=headers,
        data=data,
        files=files,
        timeout=60
    )
    resp.raise_for_status()
    return resp.json()

@app.route("/query/text", methods=["POST"])
@limiter.limit("60/minute")
def query_text():
    payload = request.json
    q = payload.get("query")
    if not q:
        return jsonify({"error": "query is required"}), 400

    # 1) Retrieve relevant context via LlamaIndex (RAG)
    if index:
        query_engine = index.as_query_engine()
        resp = query_engine.query(q)

        context = str(resp)
    else:
        context = ""

    # 2) Ask HF model (plain text)
    # For text-only, send as input string
    out = call_hf_multimodal_model(image_bytes=None, prompt=f"{context}\n\nUser question: {q}")
    return jsonify({"answer": out, "context": context})

@app.route("/query/image", methods=["POST"])
@limiter.limit("30/minute")
def query_image():
    # image-based Q/A (multipart)
    if "image" not in request.files:
        return jsonify({"error": "image file required"}), 400
    image_file = request.files["image"]
    question = request.form.get("question", "Describe the image")
    image_bytes = image_file.read()

    # Optionally: run a retrieval step using image metadata or compute embedding and query index.
    # (left simple here)
    model_resp = call_hf_multimodal_model(image_bytes=image_bytes, prompt=question)
    return jsonify({"answer": model_resp})

@app.route("/health")
def health():
    return jsonify({"status": "ok", "time": time.time()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
