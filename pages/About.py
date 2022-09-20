import streamlit as st

with open("./markdown/about.md", "r") as f:
    data = f.read()
st.markdown(data, unsafe_allow_html=True)
