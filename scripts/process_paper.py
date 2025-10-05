import fitz  # PyMuPDF
import os
import json

# --- Configuration ---
DATA_DIRECTORY = "data"
OUTPUT_FILE = "processed_papers.json"

def process_all_pdfs():
    """
    Loops through all PDFs in the data directory, extracts their text,
    and saves the content to a single JSON file.
    """
    all_papers_data = []
    
    pdf_files = [f for f in os.listdir(DATA_DIRECTORY) if f.endswith('.pdf')]
    print(f"Found {len(pdf_files)} PDF files to process.")

    for filename in pdf_files:
        print(f"Processing '{filename}'...")
        pdf_path = os.path.join(DATA_DIRECTORY, filename)
        
        try:
            doc = fitz.open(pdf_path)
            full_text = ""
            for page in doc:
                full_text += page.get_text()
            doc.close()
            
            paper_data = {
                'filename': filename,
                'pmcid': filename.replace('.pdf', ''), # Use filename as an ID
                'full_text': full_text
            }
            all_papers_data.append(paper_data)
            print(f"Successfully extracted {len(full_text)} characters.")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_papers_data, f, indent=2)
        
    print(f"\nProcessing complete. All data saved to '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    process_all_pdfs()