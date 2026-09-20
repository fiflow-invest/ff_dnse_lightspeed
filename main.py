import os
import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Get the absolute path to 'openapi-sdk/python' relative to main.py
sdk_path = Path(__file__).resolve().parent / "openapi-sdk" / "python"

if str(sdk_path) not in sys.path:
    sys.path.insert(0, str(sdk_path))

