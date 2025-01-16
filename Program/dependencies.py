import os
import requests
import shutil
import zipfile
import json
import time

isReady = False

def update_dependancies(ui):
    time.sleep(0.5)
    if not os.path.exists(r"PDFs"):
        ui.updateText.text = "Προετοιμασία για πρώτη χρήση.."
        download_dependancies(ui)
    git_config_file = "https://raw.githubusercontent.com/sharl16/Trapeza_Thematwn_Searcher/main/PDFs/B/version.json"
    ui.updateText.text = "Έλεγχος για ενημερώσεις.."
    try:
        session = requests.session()
        response = session.get(git_config_file, stream=True, timeout=(5, 10)).json()
        local_json = None
        with open(r'PDFs\B\version.json') as f:
            local_json = json.load(f)
        online_json = response
        print(local_json, online_json)
        if local_json != online_json:
            ui.updateText.text = "Λήψη ενημερώσεων.."
            download_dependancies(ui)
        else:
            ui.updateText.text = "Η εφαρμογή είναι ενημερωμένη!"
    except requests.exceptions.RequestException as e:
        ui.updateText.text = f"Failed to update dependancies: {e}"

def download_dependancies(ui):
    drive_pdf_link = "https://drive.usercontent.google.com/download?id=1i9G7jwnOA66tgBqc54f-cRh7t4Yvmhqh&export=download&authuser=0&confirm=t&uuid=04e9c882-615b-4eb0-859e-34423d71a931&at=APvzH3qY6_v6jfnozoMeH-hNYr0e%3A1734253857478"
    if os.path.exists(r"PDFs"):
        shutil.rmtree(r"PDFs")

    output = os.path.join(r"PDFs")

    try:
        ui.updateText.text = "Λήψη ενημερώσεων.."
        response = requests.get(drive_pdf_link, stream=True, timeout=(10, 30))
        response.raise_for_status()
        with open(output, 'wb') as file:
            total_length = int(response.headers.get('content-length'))
            for chunk in response.iter_content(chunk_size=16384):
                file.write(chunk)
    
        ui.updateText.text = "Εγκατάσταση.."
        os.rename(r"PDFs", r"TempPDF")
        with zipfile.ZipFile(r"TempPDF", 'r') as zip_ref:
            zip_ref.extractall()
        os.remove(r"TempPDF")
        update_dependancies(ui)
    except requests.exceptions.RequestException as e:
        input(f"Failed to download libraries: {e}")
        quit()