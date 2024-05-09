# Imports of utils functions
from utils import load_glove_model, lazy_teacher_pipeline

# Imports for environment variables
import os
from dotenv import load_dotenv

# Imports for web API
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Imports for data handling and processing
import numpy as np
from PIL import Image

# Imports for type annotations
from typing import List, Dict

# Imports for deep learning and model processing
import torch
from transformers import pipeline, AutoModelForImageClassification, AutoImageProcessor


