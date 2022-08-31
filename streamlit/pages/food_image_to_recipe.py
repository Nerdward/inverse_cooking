import streamlit as st
import time
import numpy as np
import requests
import torch
import pickle
from src.predict import *
from src import generate
from pathlib import Path
import urllib.request



BASE_DIR = Path(__file__).parents[2]

@st.cache()
def load_app_artifacts():
    url = 'https://dl.fbaipublicfiles.com/inversecooking/modelbest.ckpt'
    save_dest = Path('model')
    save_dest.mkdir(exist_ok=True)
    
    f_checkpoint = Path("model/modelbest.ckpt")
    if not f_checkpoint.exists():
        with st.spinner("Downloading model... this may take awhile! \n Don't stop it!"):
            urllib.request.urlretrieve(url, f_checkpoint)
    model, ingrs_vocab, vocab = load_artifacts(ingr_path=Path(BASE_DIR, 'app/artifacts/ingr_vocab.pkl'),
    vocab_path=Path(BASE_DIR, 'app/artifacts/instr_vocab.pkl'),
    model_path=f_checkpoint)
    
    return model, ingrs_vocab, vocab

def _predict(file):
    model, ingrs_vocab, vocab = load_app_artifacts()
    image = load_image(file.read())

    primage = preprocess(image)

    recipe = predict(model, ingrs_vocab, vocab, primage)

    return recipe

st.set_page_config(page_title="Recipe_to_image", page_icon="🤖")
st.markdown("# Image to Recipe")
st.sidebar.header("Image to Recipe")

st.write(
    """
    This model requires you to input a picture of an already
    prepared meal and it will produce the recipe of the meal
    """
)

col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("Choose a file",type=['png','jpeg','jpg'])
    
with col2:
    img_file_buffer = st.camera_input("Take a picture of the food")

if st.button("Generate"):
    with st.spinner("Generating the recipe:"):
        if uploaded_file is not None:
            response = _predict(uploaded_file)
            st.json(response)
        else:
            response = _predict(uploaded_file)
            st.json(response)
# print(type(uploaded_file))
# print(uploaded_file)