import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from main import app
    from model import models
    print("Successfully imported app and models")
    print(f"Loaded models: {list(models.keys())}")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
