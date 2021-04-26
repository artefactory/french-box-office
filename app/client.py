import streamlit as st
import requests
import json

st.title("Welcome to the ENPC Movie Predictor!")
movie_title = st.text_input("Please enter the title of the movie you want to predict Box Office Sales on :")

if st.button('Send request to API'):
    res = requests.post('http://0.0.0.0:8080/predict', json={'movie_title': movie_title})
    content = json.loads(res.content)
    if res.status_code == 200:
        st.success(f"Movie '{content['original_title']}' ({content['year']}) forecasted sales: {content['box_office_sales_forecast']}")
    elif res.status_code == 404:
        st.error(f"{content['detail']}")
