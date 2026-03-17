import chromadb
from chromadb.utils import embedding_functions
import os

# --- CONFIGURATION ---
# This creates a folder named 'chroma_memory' inside your project to save data
PERSIST_DIRECTORY = os.path.join(os.getcwd(), "chroma_memory")

def get_vector_db():
    """
    Initializes the local Vector Database (ChromaDB).
    Uses the free 'all-MiniLM-L6-v2' model for embeddings.
    """
    print("Connecting to Vector Memory ---")
    
    # 1. Setup the Client (Persistent = saves to disk)
    client = chromadb.PersistentClient(path=PERSIST_DIRECTORY)
    
    # 2. Define the "Translator" (Embedding Function)
    # This automatically downloads a small, free AI model to your laptop
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    # 3. Get or Create the Collection (The "Folder" for memories)
    collection = client.get_or_create_collection(
        name="viki_memories",
        embedding_function=embedding_func
    )
    
    return collection

# --- TEST BLOCK ---
if __name__ == "__main__":
    # If you run this file directly, it tests the system
    col = get_vector_db()
    print(f"✅ Vector DB is ready! Saving data to: {PERSIST_DIRECTORY}")