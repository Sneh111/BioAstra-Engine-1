import json
import ollama # Make sure you have run: pip install ollama

# --- Configuration ---
INPUT_FILE = "processed_papers.json"
MODEL_NAME = "llama3" # The Ollama model to use

# --- Main Logic ---

def get_summary(text_content):
    """Sends text to the local Ollama model and gets a summary."""
    try:
        # We shorten the text to ensure it fits well within the model's context
        # 12,000 characters is a safe length for many models.
        truncated_text = text_content[:12000]
        
        # This is the instruction (prompt) we give to the AI model.
        # Being specific and clear in the prompt leads to better results.
        prompt = f"""
        You are an expert science communicator specializing in space bioscience. 
        Summarize the key findings of the following research paper text in three clear bullet points.
        Focus on the main results and their implications for space exploration.
        ---
        TEXT:
        {truncated_text}
        ---
        """
        
        # This sends the request to your local Ollama model.
        # The script will wait here until the model finishes generating a response.
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        # The summary is inside the 'content' of the 'message' in the response dictionary.
        return response['message']['content']

    except Exception as e:
        # This error message will appear if the script can't connect to Ollama.
        return f"An error occurred: {e}. Is the Ollama application running on your computer?"

# --- This is the main part of the script that runs when you execute the file ---
if __name__ == "__main__":
    # Load the paper data you created with the process_paper.py script.
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            papers = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{INPUT_FILE}' was not found. Please run 'process_paper.py' first.")
        papers = [] # Set papers to an empty list to prevent further errors

    # Check if there are any papers to process.
    if papers:
        # Get the text of the first paper to use as a test.
        first_paper_text = papers[0]['full_text']
        pmcid = papers[0]['pmcid']
        
        print(f"Requesting AI summary for paper: {pmcid} using local model '{MODEL_NAME}'...")
        
        # Call our function to generate the summary.
        summary = get_summary(first_paper_text)
        
        # Print the final result.
        print("\n--- AI Generated Summary (Local Model) ---")
        print(summary)
        print("----------------------------------------")