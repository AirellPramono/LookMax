import os
from openai import OpenAI
import streamlit as st
import requests
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import numpy as np
import base64
import tempfile
import io
import google.generativeai as genai
import json

load_dotenv()


genai.configure(api_key= os.environ.get('GOOGLE_API_KEY'))
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
weatherbit_api_key = os.environ.get('WEATHERBIT_API_KEY')

# def story(prompt):

#     genai.configure(api_key= os.environ.get('GOOGLE_API_KEY'))
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     response = model.generate_content(("Create a storybook based on the topic of " + prompt ))
#     return response.text

# def cover(story):
#   response = client.images.generate(
#   model="dall-e-2",
#   prompt="Make a storybook cover based on story below, and the main character face shown as front facing in the cover\n" + story,
#   size="512x512",
#   quality="standard",
#   n=1,
# )

#   image_url = response.data[0].url

#   return image_url

# def storybook(prompt):
#   narration = story(prompt)
# #   st.image(cover(narration))
#   st.write(narration)

# title = st.text_input("")

# if st.button("Generate"):
#     st.write(story(title))
def get_weather(city, api_key):
    url = f"http://api.weatherbit.io/v2.0/current?city={city}&key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temperature = data['data'][0]['temp']
        weather_description = data['data'][0]['weather']['description']
        return temperature, weather_description
    else:
        st.error("Error fetching weather data!")
        return None, None

def check_fit(img):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": """You are a detailed wardrobe advisor.
            Your job is to analyze clothes, recommend up to date fashion trends, and keeping all of them in a format very suitable for fashion.
            The output should be in python dictionaries with details of the clothes as well. Don't display the ```python``` in the result. Also the result should not contain accessories.
            This is example of the format that we need for each 
    {
      "type": "jeans",
      "color": "blue",
      "material": "denim",
      "description": "A classic crew neck t-shirt, short-sleeved, offering a simple and casual look.",

    },

    Output should be like above, not like {\n  \"top\": {\n    \"type\": \"jacket\",\n    \"color\": \"black\",\n}
            """,
        },
        {
            "role": "user",
            "content": [
                {"type":"text","text":"Describe the fashion or clothes worn in the image from top to bottom."},
                {"type":"image_url",
                 "image_url":{"url":f"data:image/png;base64,{img}"
                },}
            ],
        },

    ],
    max_tokens = 750,
    n = 1


)
    result = response.choices[0].message.content
    return result

def recommender(wardrobe, occassion,temperature,weather_description):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": """You are a detailed wardrobe advisor. Your job is to recommend outfits from a person's wardrobe collection based on the occasion. Please focus only on the clothing items (top, middle, bottom). The result should not contain any accessories.
                        When recommending outfits, consider the 'type', 'color', 'material', and 'description' of the clothing.
                        For the given occasion, suggest the most appropriate combination of clothing items that would fit well together for the event."""
        },
        {
            "role": "user",
            "content": [
                {"type":"text","text":"""Below is a person's full wardrobe collection. 
                Based on this collection, please recommend a suitable outfit for the occasion of """ + occassion + 
                f""" The current weather conditions are:
                - Temperature: {temperature}°C
                - Weather description: {weather_description}.
                Provide detailed advice on how to dress appropriately for this occasion and weather."""},
                # {"type":"text","text":"Below is a person's full wardrobe collection. Tell me details of every clothes."},
                {"type":"text", "text": wardrobe},
            ],
        },
    ],
    max_tokens = 750,
    n = 1
    )

    return response.choices[0].message.content
def wishlist(missing_item):
  response = client.images.generate(
    model="dall-e-3",
    prompt="You are a fashion advisor. The fashion should be trendy, up-to-date, and aesthetically pleasing. Based on the prompt result below, the guy/girl doesn't have certain clothes that are needed for certain occassion. Make an image of clothes needed, worn by a male model" + missing_item,
    size="1024x1024",
    quality="standard",
    n=1,
  )
  image_url = response.data[0].url

  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": """You are a detailed wardrobe advisor."""
        },
        {
            "role": "user",
            "content": "You are a fashion advisor. The fashion should be trendy, up-to-date, and aesthetically pleasing. Based on the prompt result below, the guy/girl doesn't have certain clothes that are needed for certain occassion. Describe the missing clothes needed." + missing_item
        },
    ],
    max_tokens = 750,
    n = 1
    )

  wishlist_desc = response.choices[0].message.content
  
  return image_url, wishlist_desc

def store_fit(fit):
    if os.path.exists("data.json") and os.path.getsize("data.json") > 0:    
        with open("data.json", 'r') as json_file:
            data_list = json.load(json_file)
    # Parse the content from JSON string to a Python dictionary
    else:
        data_list = []
        # Now content is a dictionary. Add the new data
    data_list.append(fit)
    with open('data.json', 'w') as json_file:
        json.dump(data_list, json_file, indent=4)

enable = st.checkbox("Enable camera")
picture = st.camera_input("Take a picture", disabled=not enable)

if picture is not None:
    img = Image.open(picture).convert("RGBA")

    # Convert image to Base64
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")  # Ensure it's saved as PNG or other supported format
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image:
        temp_image.write(base64.b64decode(img_base64))
        temp_image.flush()


# DALL-E-3
# response = client.images.generate(
#   model="dall-e-3",
#   prompt="You are a fashion advisor. The fashion should be trendy, up-to-date, and aesthetically pleasing. Make a male model picture that is wearing Uniqlo white Tshirt, etc",
#   size="1024x1024",
#   quality="standard",
#   n=1,
# )
# image_url = response.data[0].url

# print(image_url)
city = st.text_input("Enter your city for weather-based recommendations:")
occassion = st.text_input("What is the occassion?")

if st.button("Generate"):
    temperature, weather_description = get_weather(city, weatherbit_api_key)
    # current_fit = check_fit(img_base64)
    # store_fit(current_fit)
    with open("data.json", 'r') as json_file:
        data_list = json.load(json_file)
        dl_asstring = str(data_list)
        print(data_list)
        recommendation = recommender(dl_asstring, occassion,temperature,weather_description)
    st.write(recommendation)
    img_url, wishlist_desc = wishlist(recommendation)
    st.image(img_url)
    st.write(wishlist_desc)







        # Use the temporary file in the OpenAI request
# if st.button("Generate"):
#     with open(temp_image.name, "rb") as image_file:
#         response = client.images.edit(
#             model="dall-e-2",
#             image=image_file,
#             mask=open("/Users/arell/Documents/untitled folder/empty.png", "rb"),  # Assuming you want to apply edits to the whole image
#             prompt="Change the colour of the shirt to green. This is for wardrobe selection purpose",
#             n=1,
#             size="512x512"                )
#     image_url = response.data[0].url
#     st.write(image_url)