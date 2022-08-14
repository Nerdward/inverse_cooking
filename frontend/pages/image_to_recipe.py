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

uploaded_file = st.file_uploader("Choose a file",type=['png','jpeg','jpg'])

st.write(" ### 0R")

img_file_buffer = st.camera_input("Take a picture of the food")

if st.button("Generate"):
    if uploaded_file is not None:
        files = {"file": uploaded_file.getvalue()}
        response = requests.post('http://127.0.0.1:8000/predict',files=files)
        recipe = response.text
        st.success(f'The generated recipe is \n{recipe}')
    else:
        files = {"file": img_file_buffer.getvalue()}
        response = requests.post('http://127.0.0.1:8000/predict',files=files)
        recipe = response.text
        st.success(f'The generated recipe is \n{recipe}')
# print(type(uploaded_file))
# print(uploaded_file)