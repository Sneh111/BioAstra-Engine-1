from flask import Flask, request, jsonify, send_from_directory
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import ollama # <-- Add ollama import

# --- Load all our data and models at startup ---
print("Loading models and data...")

with open('processed_papers.json', 'r', encoding='utf-8') as f:
    papers_data = json.load(f)
papers_dict = {p['pmcid']: p for p in papers_data}

index = faiss.read_index('paper_index.faiss')

with open('paper_ids.json', 'r') as f:
    paper_ids = json.load(f)

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

print("Server is ready to accept requests.")
# --- End of startup loading ---

app = Flask(__name__, static_folder='frontend', static_url_path='')


# --- NEW: Summarization Function ---
def get_summary(text_content):
    """Sends text to the local Ollama model and gets a summary."""
    try:
        truncated_text = text_content[:12000]
        prompt = f"""
        You are an expert science communicator specializing in space bioscience. 
        Summarize the key findings of the following research paper text in three clear bullet points.
        Focus on the main results and their implications for space exploration.
        ---
        TEXT:
        {truncated_text}
        ---
        """
        response = ollama.chat(
            model='phi3:mini', # Or 'phi3:mini' if you are using that one
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']
    except Exception as e:
        return f"An error occurred: {e}. Is the Ollama application running?"


# --- API Endpoint for Searching ---
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Query parameter 'q' is required."}), 400

    print(f"Received search query: '{query}'")
    query_embedding = embedding_model.encode([query])
    query_embedding = np.array(query_embedding, dtype=np.float32)

    k = 5
    distances, indices = index.search(query_embedding, k)

    results = []
    for i in range(k):
        paper_index = indices[0][i]
        paper_id = paper_ids[paper_index]
        paper_info = papers_dict.get(paper_id)
        
        if paper_info:
            results.append({
                "pmcid": paper_info['pmcid'],
                "snippet": paper_info['full_text'][:300] + "..."
            })
    return jsonify(results)


# --- NEW: API Endpoint for Summarizing ---
@app.route('/summarize', methods=['GET'])
def summarize():
    paper_id = request.args.get('id', '')
    if not paper_id:
        return jsonify({"error": "ID parameter is required."}), 400
    
    print(f"Received summarization request for: '{paper_id}'")
    
    paper_info = papers_dict.get(paper_id)
    if not paper_info:
        return jsonify({"error": "Paper not found."}), 404

    summary = get_summary(paper_info['full_text'])
    return jsonify({"summary": summary})


# --- Route to serve the main HTML page ---
@app.route('/')
def serve_index():
    return send_from_directory('frontend', 'index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)