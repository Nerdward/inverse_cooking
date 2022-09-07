import streamlit as st
import time
import numpy as np
import requests
from src import generate
from tensorflow import keras
from PIL import Image
from io import BytesIO
import numpy as np
from skimage import transform
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
def load(filename):   
    np_image = Image.open(filename)
    np_image = np.array(np_image).astype('float32')/255
    np_image = transform.resize(np_image, (224, 224, 3))
    # np_image = np.expand_dims(np_image, axis=0)
    
    return np_image

@st.cache(persist=True)
def _generate(rawtext : str):
    text = generate.main(rawtext)
    
    return text

@st.cache()
def _ingredients(file):
    with open(Path(Path(__file__).parents[2], "app/labels.txt")) as f:
        data = f.read()
    d = json.loads(data)
    model = keras.models.load_model(Path(Path(__file__).parents[2], "classifier")) 
    tests = []
    for f in file:
        test = load(f)
        tests.append(test)
    tests = np.array(tests)
    pred = model.predict(tests, batch_size=tests.shape[0])
    pred = np.argmax(pred,axis=1)

    # Map the label
    # pred = [labels[k] for k in pred]
    text = ""
    for k in pred:
        text = text + d[str(k)] + ','
    text = text[:-1] + ';'
    # text = generate.main(text)
    return text

st.set_page_config(page_title="Ingredients to Recipe", page_icon="🤖")
st.markdown("# Ingredients to Recipe")
st.sidebar.header("Ingredients to Recipe")

st.write(
    """
    This model can take in images as input and also typed in
    values from the textbar.
    
    Upload image of cooking ingredients here
    """
)

col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=True)
# st.write(" ### 0R")

with col2:
    img_file_buffer = st.camera_input("Take a picture of an ingredient")
if uploaded_file or img_file_buffer is not None:
    if st.button("Generate"):
        with st.spinner('Generating recipes'):
            if uploaded_file is not None:
                text = _ingredients(uploaded_file)
                st.write(text)
                recipe = _generate(text)
                st.json(recipe)
            elif img_file_buffer is not None:
                recipe = _ingredients(img_file_buffer)
                st.write(text)
                recipe = _generate(text)
                st.json(recipe)

st.write(
    """
    Users can also type in the ingredients manually.
    """
)

with open(Path(BASE_DIR, "ingredients.npy"), 'rb') as f:
    ing = np.load(f)

# title = st.text_input('Comma-separated ingredients',)
title = st.multiselect('Choose your ingredients',options=ing)
recommend = st.checkbox("Recommend Ingredients")
if st.button("Predict"):
    if title is not None:
        if not recommend:
            # data = {'rawtext': ','.join(title) + ';'}
            # print(title)
            # print(data)
            # response = requests.post('http://127.0.0.1:8000/generate',params=data)
            recipe = _generate(','.join(title) + ';')
            st.json(recipe)
        else:
            # data = {'rawtext': title}
            # print(title)
            # print(data)
            # response = requests.post('http://127.0.0.1:8000/generate',params=data)
            recipe = _generate(','.join(title))
            st.json(recipe)
