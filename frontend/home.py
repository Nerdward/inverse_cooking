import streamlit as st

st.set_page_config(
    page_title="FoodAI home",
    page_icon="👋",
)

st.write("# Welcome to FoodAI! 👋")

st.sidebar.success("Select a model above.")

st.markdown(
    """
    FoodAI is a project from Hamoye that uses AI to assist you in
    the kitchen. It can also generate recipes of food from just
    images of the meal.  **👈 Select a model from the sidebar** to
    see what it can do.
    
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
"""
)