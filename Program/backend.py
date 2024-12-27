import os
import fitz
import re

def index_pdf(folder_path, word):
    results = []  # Use a local list
    word_to_find = normalize_text(word.lower())

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            index_pdf_backend(file_path, filename, word_to_find, results)
    
    return results

def normalize_text(text):
    text = re.sub(r'\s+', ' ', text)  
    text = text.strip()  
    return text

def index_pdf_backend(file_path, filename, word_to_find, results):
    print(f"Θέμα: {filename}", end='\r', flush=True)
    try:
        with fitz.open(file_path) as pdf_document:
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                text = page.get_text()

                if text:
                    normalized_text = normalize_text(text.lower())
                    if word_to_find in normalized_text:
                        results.append(filename)
                        break
    except Exception as e:
        print(f"Error reading {filename}: {e}")
