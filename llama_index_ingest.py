import os
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Directories
DATA_DIR = "data"
PERSIST_DIR = "index_store"

# Ensure data folder exists
os.makedirs(DATA_DIR, exist_ok=True)

# Create a sample file if not present
sample_path = os.path.join(DATA_DIR, "sample.txt")
if not os.path.exists(sample_path):
    with open(sample_path, "w", encoding="utf-8") as f:
        f.write("This is a sample document for testing the LlamaIndex chatbot integration.")

print(f"Data folder ready: {os.path.abspath(DATA_DIR)}")

def build_index():
    print(" Loading documents...")
    reader = SimpleDirectoryReader(DATA_DIR)
    docs = reader.load_data()

    print("Initializing Hugging Face embedding model...")
    # Replace below with your own model if you uploaded it (e.g., "SafaPS/qwen-local")
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Set global embedding model so LlamaIndex never calls OpenAI
    Settings.embed_model = embed_model
    Settings.llm = None  #  disables OpenAI fallback LLM

    print("Creating vector index...")
    index = VectorStoreIndex.from_documents(docs)

    print(f"Saving index to: {os.path.abspath(PERSIST_DIR)}")
    os.makedirs(PERSIST_DIR, exist_ok=True)
    index.storage_context.persist(persist_dir=PERSIST_DIR)

    print("Index successfully built and saved using Hugging Face embeddings!")

if __name__ == "__main__":
    build_index()

