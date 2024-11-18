import streamlit as st
from openai import OpenAI
import os
import main as m
import json
from PIL import Image


client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
weatherbit_api_key = os.environ.get('WEATHERBIT_API_KEY')

st.title("Wardrobe")

image_files = [f for f in os.listdir("/") if f.startswith(('captured'))]

num_columns = 3  # Define how many images per row
columns = st.columns(num_columns)

for i, image_file in enumerate(image_files):
        # Open and display the image in the appropriate column
        image_path = os.path.join("wardrobe_img", image_file)
        image = Image.open(image_path)
        
        with columns[i % num_columns]:
            st.image(image, use_container_width=True)

with open("data.json", 'r') as json_file:
    data_list = json.load(json_file)
    dl_asstring = str(data_list)    
    st.write(m.describe_wardrobe(dl_asstring,client))