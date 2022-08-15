import streamlit as st
import time
import numpy as np
import requests

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
            files = {"file": uploaded_file.getvalue()}
            response = requests.post('http://127.0.0.1:8000/predict',files=files)
            recipe = response.text
            st.json(recipe)
        else:
            files = {"file": img_file_buffer.getvalue()}
            response = requests.post('http://127.0.0.1:8000/predict',files=files)
            recipe = response.text
            st.json(recipe)
# print(type(uploaded_file))
# print(uploaded_file)