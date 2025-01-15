"""
A backend for app.py. 
It gets the folder of a subject to search by app.py, and then
using pypdfium2 it initiates a search. Cross-Compatible with
Windows & Android.
"""

import os
import pypdfium2 as pdfium # replaced PyMuPDF to pypdfium2 for cross-platform compatibility
import re

# remains the same from PyMuPDF.
# wrapper function to index_pdf_backend
def index_pdf(folder_path, word):
    results = []  # pdf files that match save their filename as a string: (e.x. 14791.pdf) 
    word_to_find = normalize_text(word.lower())

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            index_pdf_backend(file_path, filename, word_to_find, results)
    
    return results # return to app.py

def normalize_text(text):
    text = re.sub(r'\s+', ' ', text)  
    text = text.strip()  
    return text

def index_pdf_backend(file_path, filename, word_to_find, results):
    print(f"Θέμα: {filename}", end='\r', flush=True) # debugging information
    try:
        with open(file_path, 'rb') as file: # opens pdf file in binary mode ('rb')
            pdf = pdfium.PdfDocument(file) # initializes pdf file with pdfium2
            n_pages = len(pdf)
            page = pdf[0]
            textpage = page.get_textpage() # load a text page helper, whatever that is
            text_doc = textpage.get_text_range() # extract text from page
            # search for matches
            searcher = textpage.search(word_to_find, match_case = False, match_whole_word = False)
            first_occurrence = searcher.get_next()
            if first_occurrence:
                results.append(filename) # add filename to results[]
    except Exception as e:
        print(f"Error reading {filename}: {e}")