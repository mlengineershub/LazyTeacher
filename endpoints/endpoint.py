# Imports for environment variables
from fastapi import FastAPI
import uvicorn

import os
from dotenv import load_dotenv

# Load environment variables
ENV_FILE_PATH = (
    os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
)
load_dotenv(dotenv_path=ENV_FILE_PATH)

host = os.getenv("HOST")
port = int(os.getenv("PORT_ENDPOINT"))
app_port = int(os.getenv("PORT_APP"))

# Initialize the FastAPI app
app = FastAPI()


# Define the endpoints
@app.get("/")
async def index():
    return {"message":
            "Hello, please go to /docs to see the API documentation"}


if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)
