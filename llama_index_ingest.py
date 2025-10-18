# import os
# from llama_index.core import (
#     VectorStoreIndex,
#     SimpleDirectoryReader,
#     StorageContext
# )
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding


# # ✅ Directories
# DATA_DIR = "data"
# PERSIST_DIR = "index_store"

# # ✅ Make sure the data folder exists
# os.makedirs(DATA_DIR, exist_ok=True)

# # ✅ Create a sample file if not present
# sample_path = os.path.join(DATA_DIR, "sample.txt")
# if not os.path.exists(sample_path):
#     with open(sample_path, "w", encoding="utf-8") as f:
#         f.write("This is a sample document for testing the LlamaIndex chatbot integration.")

# print(f"📁 Data folder ready: {os.path.abspath(DATA_DIR)}")

# # ✅ Function to build index
# def build_index():
#     print("🚀 Loading documents...")
#     reader = SimpleDirectoryReader(DATA_DIR)
#     docs = reader.load_data()

#     print("🧠 Creating embedding model...")
#     embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")



#     print("📦 Creating vector index...")
#     index = VectorStoreIndex.from_documents(docs, embed_model=embed_model)

#     print("💾 Saving index to:", PERSIST_DIR)
#     os.makedirs(PERSIST_DIR, exist_ok=True)
#     index.storage_context.persist(persist_dir=PERSIST_DIR)

#     print("✅ Index successfully built and saved!")

# if __name__ == "__main__":
#     build_index()

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

# Make sure data folder exists
os.makedirs(DATA_DIR, exist_ok=True)

# Create a sample file if not present
sample_path = os.path.join(DATA_DIR, "sample.txt")
if not os.path.exists(sample_path):
    with open(sample_path, "w", encoding="utf-8") as f:
        f.write("This is a sample document for testing the LlamaIndex chatbot integration.")

print(f" Data folder ready: {os.path.abspath(DATA_DIR)}")

def build_index():
    print(" Loading documents...")
    reader = SimpleDirectoryReader(DATA_DIR)
    docs = reader.load_data()

    print(" Creating Hugging Face embedding model...")
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Register embedding model globally with new Settings system
    Settings.embed_model = embed_model

    print("Creating vector index...")
    index = VectorStoreIndex.from_documents(docs)

    print(" Saving index to:", PERSIST_DIR)
    os.makedirs(PERSIST_DIR, exist_ok=True)
    index.storage_context.persist(persist_dir=PERSIST_DIR)

    print("Index successfully built and saved using HuggingFace embeddings!")

if __name__ == "__main__":
    build_index()

