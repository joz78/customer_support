"""Root app entry point for Hugging Face Spaces deployment"""
import subprocess
import sys

if __name__ == "__main__":
    # Run uvicorn with the FastAPI app
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "api.main:app",
        "--host", "0.0.0.0",
        "--port", "7860"
    ])
