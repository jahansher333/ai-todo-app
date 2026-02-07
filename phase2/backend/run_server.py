from main import app
import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))  # Hugging Face Spaces uses port 7860
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)
