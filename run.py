import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import app
import uvicorn

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    os.makedirs("config", exist_ok=True)
    
    # Run the server
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
