from fastapi import FastAPI, Request, Response
import uvicorn
import sys
import os
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from pydantic import BaseModel
from starlette.responses import JSONResponse
from textSummarizer.pipeline.prediction import PredictionPipeline
from fastapi.staticfiles import StaticFiles


class TextInput(BaseModel):
    text: str

text:str = "What is Text Summarization?"

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", tags=["authentication"])
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/summarizer")
async def summarizer(request: Request):
    return templates.TemplateResponse("summarize.html", {"request": request})

@app.get("/train")
async def training():
    try:
        os.system("python main.py")
        return Response("Training successful !!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")
    
@app.post("/predict")
async def predict_route(request: Request):
    try:
        data = await request.json()
        text = data.get("text_input")

        obj = PredictionPipeline()
        summary = obj.predict(text)

        summary = summary.replace("<n>", "\n")

        return JSONResponse(content={"data": summary})
    except Exception as e:
        return JSONResponse(content={"error": f"Error Occurred! {e}"}, status_code=500)

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)