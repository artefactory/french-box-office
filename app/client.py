import streamlit as st
import requests

name = st.text_input("Please enter your name:")
if st.button('Send request to API'):
    res = requests.post('http://0.0.0.0:8080/predict', json={'user': name})
    st.write(res.content)