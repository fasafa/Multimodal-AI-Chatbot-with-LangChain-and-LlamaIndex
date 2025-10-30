import os
import io
import time
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from PIL import Image
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    AutoProcessor,
    BlipForConditionalGeneration
)
import torch

app = Flask(__name__)

# ----------------------------------
# RATE LIMITER
# ----------------------------------
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

# ----------------------------------
# LOAD LOCAL TEXT MODEL (Qwen or Phi)
# ----------------------------------
TEXT_MODEL_NAME = "Qwen/Qwen2-0.5B-Instruct"

print(f"Loading text model: {TEXT_MODEL_NAME}...")
text_tokenizer = AutoTokenizer.from_pretrained(TEXT_MODEL_NAME)
text_model = AutoModelForCausalLM.from_pretrained(
    TEXT_MODEL_NAME,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)
text_model.to("cuda" if torch.cuda.is_available() else "cpu")
print("Text model loaded successfully ")

# ----------------------------------
# LOAD LOCAL IMAGE MODEL (BLIP)
# ----------------------------------
IMG_MODEL_NAME = "Salesforce/blip-image-captioning-base"

print(f"Loading image model: {IMG_MODEL_NAME}...")
img_processor = AutoProcessor.from_pretrained(IMG_MODEL_NAME)
img_model = BlipForConditionalGeneration.from_pretrained(IMG_MODEL_NAME)
print("Image model loaded successfully ")

# ----------------------------------
# TEXT QUERY ROUTE
# ----------------------------------
@app.route("/query/text", methods=["POST"])
@limiter.limit("60/minute")
def query_text():
    payload = request.json
    q = payload.get("query")
    if not q:
        return jsonify({"error": "query is required"}), 400

    # Improved system prompt for conversational tone
    full_prompt = (
        f"You are a helpful AI assistant. "
        f"Please answer the user's question clearly and concisely.\n\n"
        f"User: {q}\nAssistant:"
    )

    inputs = text_tokenizer(full_prompt, return_tensors="pt").to(text_model.device)
    outputs = text_model.generate(**inputs, max_new_tokens=200, temperature=0.7)
    answer = text_tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Clean unwanted prefix if present
    answer = answer.replace(full_prompt, "").strip()

    return jsonify({"answer": answer})

# ----------------------------------
# IMAGE QUERY ROUTE
# ----------------------------------
@app.route("/query/image", methods=["POST"])
@limiter.limit("30/minute")
def query_image():
    if "image" not in request.files:
        return jsonify({"error": "image file required"}), 400

    image_file = request.files["image"]
    image_bytes = image_file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    question = request.form.get("question", "Describe this image.")
    
    # Preprocess image + question for BLIP
    inputs = img_processor(image, text=question, return_tensors="pt")

    # Generate caption
    output_ids = img_model.generate(**inputs, max_new_tokens=80)
    caption = img_processor.batch_decode(output_ids, skip_special_tokens=True)[0]
    caption = caption.strip()

    return jsonify({"answer": caption})

# ----------------------------------
# HEALTH CHECK
# ----------------------------------
@app.route("/health")
def health():
    return jsonify({"status": "ok", "time": time.time()})

# ----------------------------------
# RUN APP
# ----------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
