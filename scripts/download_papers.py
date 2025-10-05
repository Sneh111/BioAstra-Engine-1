import os
import csv
import requests # Make sure you have run: pip install requests

# --- Configuration ---

# The name of the CSV file you downloaded
CSV_FILENAME = "SB_publication_PMC.csv" # TODO: Make sure this name matches your downloaded file!

# The name of the column in the CSV that contains the PDF URLs
# Inspect your CSV file to find the correct column header name!
URL_COLUMN_NAME = "pdf_link" # TODO: Change this if the column name is different!

# The folder where you want to save the PDFs
SAVE_DIRECTORY = "data"


# --- Main Download Logic ---

def get_publication_urls():
    """Reads the CSV file and extracts all URLs from the specified column."""
    urls = []
    # --- FIX #1: Change the column name here ---
    URL_COLUMN_NAME = "Link"

    try:
        # --- FIX #2: Change the encoding here to handle the hidden character ---
        with open(CSV_FILENAME, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # This debug line is no longer needed but is fine to keep for now
            print(f"DEBUG: CSV Headers are: {reader.fieldnames}")
            
            for row in reader:
                if URL_COLUMN_NAME in row and row[URL_COLUMN_NAME]:
                    urls.append(row[URL_COLUMN_NAME])
    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILENAME}' was not found in the project directory.")
        return None
    except KeyError:
        print(f"Error: The CSV file does not have a column named '{URL_COLUMN_NAME}'.")
        return None
        
    return urls

import time # Import the time library

# (Make sure 'os', 'csv', and 'requests' are also imported at the top of the file)
from bs4 import BeautifulSoup # Import BeautifulSoup

import time
from bs4 import BeautifulSoup
import os
import requests
import csv

# (Ensure all other parts of your script like SAVE_DIRECTORY and get_publication_urls are still there)

import time
from bs4 import BeautifulSoup
import os
import requests
import csv

# (Ensure all other parts of your script are still there)

import time
from bs4 import BeautifulSoup
import os
import requests
import csv

# (Ensure all other parts of your script are still there)

import time
from bs4 import BeautifulSoup
import os
import requests
import csv

# (Ensure all other parts of your script are still there)

import time
from bs4 import BeautifulSoup
import os
import requests
import csv
from urllib.parse import urljoin # <-- IMPORTANT: Add this import

import time
from bs4 import BeautifulSoup
import os
import requests
import csv
from urllib.parse import urljoin

import time
from bs4 import BeautifulSoup
import os
import requests # Make sure requests is imported
import csv
from urllib.parse import urljoin

def download_publications(publication_urls):
    """
    Uses a persistent session to handle cookies and download the correct PDF file.
    """
    if not publication_urls:
        print("No URLs found to download. Exiting.")
        return
    SAVE_DIRECTORY = "data"
    if not os.path.exists(SAVE_DIRECTORY):
        os.makedirs(SAVE_DIRECTORY)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # --- THE FIX IS HERE: Create a Session object ---
    session = requests.Session()
    session.headers.update(headers)

    print(f"Starting download of {len(publication_urls)} publications...")

    for article_url in publication_urls:
        try:
            filename_base = article_url.rstrip('/').split('/')[-1]
            filename = filename_base + '.pdf'
            save_path = os.path.join(SAVE_DIRECTORY, filename)

            if os.path.exists(save_path):
                print(f"'{filename}' already exists. Skipping.")
                continue

            # Step 1: Visit the page using the session to get cookies
            page_response = session.get(article_url, timeout=30)
            page_response.raise_for_status()
            
            soup = BeautifulSoup(page_response.content, 'html.parser')
            
            selectors_to_try = [
                "a.icn-action-button.download", "a[title='Download PDF']", "ul.format-menu a[href$='.pdf']",
                "div.format-menu a[href$='.pdf']", "a.pdf-link", "a[ga-action='pdf']", "a[href*='/pdf/']"
            ]
            pdf_link_tag = None
            for selector in selectors_to_try:
                pdf_link_tag = soup.select_one(selector)
                if pdf_link_tag: break
            if not pdf_link_tag or not pdf_link_tag.has_attr('href'):
                print(f"Could not find a PDF link on page: {article_url}. Skipping.")
                continue
            
            pdf_href = pdf_link_tag['href']
            pdf_url = urljoin(article_url, pdf_href)

            print(f"Found PDF link: {pdf_url}. Requesting download...")
            
            # Step 2: Download the PDF using the same session (which now has the cookies)
            pdf_response = session.get(pdf_url, timeout=60, stream=True)
            pdf_response.raise_for_status()

            content_type = pdf_response.headers.get('content-type')
            if 'application/pdf' not in content_type:
                print(f"Error: Did not receive a PDF for '{filename}'. Received '{content_type}'. Skipping.")
                continue

            with open(save_path, 'wb') as f:
                for chunk in pdf_response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Successfully downloaded and verified '{filename}'")
            time.sleep(1)

        except Exception as e:
            print(f"An error occurred for {article_url}: {e}")
# --- Run the Script ---

if __name__ == "__main__":
    urls = get_publication_urls()

    print(f"DEBUG: Found {len(urls) if urls else 0} URLs.")

    if urls:
        download_publications(urls)