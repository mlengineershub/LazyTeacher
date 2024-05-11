# Imports for environment variables
import io
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pytesseract
from PIL import Image
import uvicorn

import os
from dotenv import load_dotenv

# for windows users
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

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

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[f"http://{host}:{app_port}"],
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Define the endpoints
@app.get("/")
async def index():
    return {"message":
            "Hello, please go to /docs to see the API documentation"}


@app.post("/upload/")
async def create_upload_file(image: UploadFile = File(...)):
    image_data = await image.read()
    image_pil = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image_pil)
    return JSONResponse(content={"text": text})
    return {"message": "Fichier reçu"}


if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)
