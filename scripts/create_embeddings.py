import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# --- Configuration ---
INPUT_FILE = "processed_papers.json"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2" # A fast and effective model for embeddings
FAISS_INDEX_FILE = "paper_index.faiss" # The file where the search index will be saved
PAPER_IDS_FILE = "paper_ids.json" # A file to map index positions back to paper IDs

# --- Main Logic ---

def create_search_index():
    """
    Loads processed papers, generates text embeddings, and saves them into a FAISS index.
    """
    print("Loading processed papers...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        papers = json.load(f)

    # We will embed the first part of the text for efficiency
    # For a real application, you might embed chunks, but this is great for a hackathon
    texts_to_embed = [p['full_text'][:2000] for p in papers]
    paper_ids = [p['pmcid'] for p in papers]

    print(f"Loading the embedding model: '{EMBEDDING_MODEL_NAME}'...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    print("Generating embeddings for all papers... (This might take a few minutes)")
    # This creates a vector (list of numbers) for each paper's text
    embeddings = model.encode(texts_to_embed, show_progress_bar=True)

    # The dimension of our embeddings (e.g., 384 for the chosen model)
    d = embeddings.shape[1] 

    print(f"Creating a FAISS index with dimension {d}...")
    # Create the search index
    index = faiss.IndexFlatL2(d)
    
    # Add our paper embeddings to the index
    index.add(np.array(embeddings, dtype=np.float32))

    print(f"Saving FAISS index to '{FAISS_INDEX_FILE}'...")
    faiss.write_index(index, FAISS_INDEX_FILE)

    print(f"Saving paper ID mapping to '{PAPER_IDS_FILE}'...")
    with open(PAPER_IDS_FILE, 'w') as f:
        json.dump(paper_ids, f)
        
    print("\nSearch index creation complete!")

# --- Run the Script ---
if __name__ == "__main__":
    create_search_index()