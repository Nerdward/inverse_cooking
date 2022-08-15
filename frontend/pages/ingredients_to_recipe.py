import streamlit as st
import time
import numpy as np
import requests

st.set_page_config(page_title="Ingredients to Recipe", page_icon="🤖")
st.markdown("# Ingredients to Recipe")
st.sidebar.header("Ingredients to Recipe")

st.write(
    """
    This model can take in images as input and also typed in
    values from the textbar.
    """
)

col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("Choose a file")
# st.write(" ### 0R")

with col2:
    img_file_buffer = st.camera_input("Take a picture of an ingredient")
if st.button("Generate"):
    with st.spinner('Generating recipes'):
        if uploaded_file is not None:
            files = {"file": uploaded_file.getvalue()}
            response = requests.post('http://127.0.0.1:8000/ingredients',files=files)
            recipe = response.text
            st.success(f'The generated recipe is \n{recipe}')
        else:
            files = {"file": img_file_buffer.getvalue()}
            response = requests.post('http://127.0.0.1:8000/ingredients',files=files)
            recipe = response.text
            st.success(f'The generated recipe is \n{recipe}')


st.write(
    """
    Users can also type in the ingredients manually.
    """
)


title = st.text_input('Comma-separated ingredients',)
recommend = st.checkbox("Recommend Ingredients")
if st.button("Predict"):
    if title is not None:
        if not recommend:
            data = {'rawtext': title + ';'}
            # print(title)
            # print(data)
            response = requests.post('http://127.0.0.1:8000/generate',params=data)
            recipe = response.text
            st.write(recipe)
        else:
            data = {'rawtext': title}
            # print(title)
            # print(data)
            response = requests.post('http://127.0.0.1:8000/generate',params=data)
            recipe = response.text
            st.write(recipe)
