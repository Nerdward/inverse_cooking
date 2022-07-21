from fastapi import FastAPI, File, UploadFile
from http import HTTPStatus
from typing import Dict
from src.predict import *


app = FastAPI()

@app.get("/")
def _index() -> Dict:
    """Health check"""

    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {},
    }
    return response

@app.on_event("startup")
def load_app_artifacts():
    model, ingrs_vocab, vocab = load_artifacts(ingr_path='app/artifacts/ingr_vocab.pkl',
    vocab_path='app/artifacts/instr_vocab.pkl',
    model_path='app/artifacts/modelbest.ckpt')
    
    return model, ingrs_vocab, vocab


@app.post('/predict')
async def _predict(file: UploadFile = File(...)):
    model, ingrs_vocab, vocab = load_app_artifacts()
    image = load_image(await file.read())

    primage = preprocess(image)

    recipe = predict(model, ingrs_vocab, vocab, primage)

    return recipe