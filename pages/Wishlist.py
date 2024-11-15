import streamlit as st
from openai import OpenAI
import os
import main as m
import json



client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
weatherbit_api_key = os.environ.get('WEATHERBIT_API_KEY')
with open("wishlist.json", 'r') as json_file:
            recommendation = json.load(json_file)

st.markdown('<h1>Wishlist</h1>', unsafe_allow_html=True)


    # st.write(recommendation)
img_url, wishlist_desc = m.wishlist(recommendation,client)
st.image(img_url)
st.write(wishlist_desc)