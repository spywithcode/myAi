# Ai_run.py

import webbrowser
import os

def run():
    # index.html ka path set karein
    file_path = os.path.abspath("web\index.html")
    webbrowser.open(f"file://{file_path}")

if __name__ == "__main__":
    run()
    
     