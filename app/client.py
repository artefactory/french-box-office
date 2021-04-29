import streamlit as st
import requests
import json

st.title("Welcome to the ENPC Movie Predictor!")
movie_title = st.text_input("Please enter the title of the movie you want to predict Box Office Sales on :")

if st.button('Send request to API'):
    # paste the request code here
