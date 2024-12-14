import os
import json

# Directory to store cached login data
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIRECTORY = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "data"))
CACHE_FILE_PATH = os.path.join(CACHE_DIRECTORY, "login_data.json")

def save_login_data(data):
    """Save login data to a JSON file in the specified cache directory."""
    # Ensure the directory exists; if not, create it
    if not os.path.exists(CACHE_DIRECTORY):
        os.makedirs(CACHE_DIRECTORY)

    try:
        with open(CACHE_FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Failed to save login data: {str(e)}")

def load_login_data():
    """Load cached login data from the JSON file."""
    try:
        with open(CACHE_FILE_PATH, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def clear_login_data():
    """Clear cached login data by deleting the JSON file."""
    if os.path.exists(CACHE_FILE_PATH):
        os.remove(CACHE_FILE_PATH)
