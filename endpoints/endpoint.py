# Imports for environment variables
import platform
import io
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pytesseract
from PIL import Image
import uvicorn

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

import os
from dotenv import load_dotenv

from utils import lazy_teacher_pipeline, load_glove_model

# for windows users
if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = (
        'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    )

# Load environment variables
ENV_FILE_PATH = (
    os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
)
load_dotenv(dotenv_path=ENV_FILE_PATH)

host = os.getenv("HOST")
port = int(os.getenv("PORT_ENDPOINT"))
app_port = int(os.getenv("PORT_APP"))
model_ckpt = os.getenv("MODEL_CKPT")

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

device = 'cpu'
if torch.cuda.is_available():
    device = 'cuda'
elif torch.backends.mps.is_available():
    device = 'mps'
model = AutoModelForSequenceClassification.from_pretrained(
    model_ckpt, trust_remote_code=True
).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
glove_vocab = load_glove_model()


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
    note = lazy_teacher_pipeline(text=text,
                                 model=model,
                                 tokenizer=tokenizer,
                                 glove_vocab=glove_vocab,
                                 device=device)
    return JSONResponse(content={"text": text,
                                 "note": note[0]})
    return {"message": "Fichier reçu"}


if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)
