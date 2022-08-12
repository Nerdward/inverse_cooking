from fastapi import FastAPI, File, UploadFile, Request
from http import HTTPStatus
from typing import Dict
from src.predict import *
from src import generate
from tensorflow import keras
from PIL import Image
import numpy as np
from skimage import transform
# from keras.preprocessing import image
import json

app = FastAPI(openapi_url='/studiolab/default/jupyter/openapi.json')

def load(filename):   
    np_image = Image.open(BytesIO(filename))
    np_image = np.array(np_image).astype('float32')/255
    np_image = transform.resize(np_image, (224, 224, 3))
    np_image = np.expand_dims(np_image, axis=0)


    # img_width, img_height = 224, 224
    # img = image.load_img(filename, target_size = (img_width, img_height))
    # img = image.img_to_array(img)
    # img = np.expand_dims(img, axis = 0)
    return np_image

@app.get("/")
def _index() -> Dict:
    """Health check"""

    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {},
    } 
    return response

@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}

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

@app.post('/generate')
def _generate(rawtext : str):
    text = generate.main(rawtext)
    
    return text

@app.post('/ingredients')
async def _ingredients(file: UploadFile = File(...)):
    with open("app/labels.txt") as f:
        data = f.read()
    d = json.loads(data)
    model = keras.models.load_model("app/classifier") 
    test = load(await file.read())
    pred = model.predict(test)
    pred = np.argmax(pred,axis=1)

    # Map the label
    # pred = [labels[k] for k in pred]
    text = ""
    for k in pred:
        text = text + d[str(k)] + ','
    text = text[:-1] + ';'
    text = generate.main(text)

    return text
        