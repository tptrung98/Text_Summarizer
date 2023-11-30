from fastapi import FastAPI
import uvicorn
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.requests import Request
from fastapi.responses import Response
from pydantic import BaseModel
from starlette.responses import JSONResponse
from textSummarizer.pipeline.prediction import PredictionPipeline
from fastapi.staticfiles import StaticFiles
from transformers import AutoTokenizer
from transformers import pipeline
import os
import torch
from transformers import AutoModelForSeq2SeqLM,AutoTokenizer

model_name ="google/pegasus-cnn_dailymail"
tokenizer =AutoTokenizer.from_pretrained(model_name)
model_pegasus = AutoTokenizer.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained("/content/tokenizer")