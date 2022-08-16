import streamlit as st
import time
import numpy as np
import requests
import torch
import pickle
from src.predict import *
from src import generate
from pathlib import Path
from src.model import get_model

BASE_DIR = Path(__file__).parents[2]

def load_artifacts_in(ingr_path, vocab_path, model_path):
    import sys; sys.argv=['']; del sys
    args = get_parser()
    args.maxseqlen = 15
    args.ingrs_only=False
    
    with open(ingr_path, "rb") as f:
        ingrs_vocab = pickle.load(f)
    with open(vocab_path, "rb") as f:
        vocab = pickle.load(f)
    # ingrs_vocab = pickle.load(open(ingr_path, 'rb'))
    # vocab = pickle.load(open(vocab_path, 'rb'))

    ingr_vocab_size = len(ingrs_vocab)
    instrs_vocab_size = len(vocab)
    model = get_model(args, ingr_vocab_size, instrs_vocab_size)
    # Load the trained model parameters

    model.load_state_dict(torch.load(model_path, map_location=map_loc))

    return model, ingrs_vocab, vocab

@st.cache()
def load_app_artifacts():
    model, ingrs_vocab, vocab = load_artifacts_in(ingr_path=Path(BASE_DIR, 'app/artifacts/ingr_vocab.pkl'),
    vocab_path=Path(BASE_DIR, 'app/artifacts/instr_vocab.pkl'),
    model_path=Path(BASE_DIR, 'app/artifacts/modelbest.ckpt'))
    
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