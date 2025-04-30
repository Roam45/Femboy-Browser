import os
import json
import subprocess

# Create default settings if not exists
if not os.path.exists("settings.json"):
    with open("settings.json", "w") as f:
        json.dump({
            "default_search_engine": "https://www.google.com/search?q="
        }, f)

# Launch the browser
subprocess.Popen(["python", "main_stable.py"])
