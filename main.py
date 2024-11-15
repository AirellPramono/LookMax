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
import json

st.cache_data.clear()
load_dotenv()

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
weatherbit_api_key = os.environ.get('WEATHERBIT_API_KEY')

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

def check_fit(img,model):
    response = model.chat.completions.create(
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

def describe_wardrobe(wardrobe,client):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": """You are a detailed wardrobe advisor.

   
            """,
        },
        {
            "role": "user",
            "content": "We have json data below of the full wardrobe of someone. Just describe the wardrobe collections in an organized manner. The result shouldn't say anything about json file." +wardrobe,
        },

    ],
    max_tokens = 750,
    n = 1


)
    result = response.choices[0].message.content
    return result

def recommender(model,base64_image):
    client = model
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
        #   "content": """
        #   You are a detailed wardrobe advisor. Your job is to recommend outfits from a person's wardrobe collection based on the occasion. Please focus only on the clothing items (top, middle, bottom). The result should not contain any accessories.
        #                 When recommending outfits, consider the 'type', 'color', 'material', and 'description' of the clothing.
        #                 For the given occasion, suggest the most appropriate combination of clothing items that would fit well together for the event.
        #                 """
        "content": """
        You are a facial analyzer. Your job is to analyze the face, skin tone, facial structure, eyes, nose, etc, in the picture. You should output a facial rating with detailed description and compare it to model looking face.
               """
        },
        {
            "role": "user",
            "content": [
                {"type":"text","text":"Analyze the face picture and give us description."},
                {"type":"image_url",
                 "image_url":{"url":f"data:image/png;base64,{base64_image}"
                },}
            ]
            # [
            #     {"type":"text","text":"""Below is a person's full wardrobe collection. 
            #     Based on this collection, please recommend a suitable outfit for the occasion of """ + occassion + 
            #     f""" The current weather conditions are:
            #     - Temperature: {temperature}°C
            #     - Weather description: {weather_description}.
            #     Provide detailed advice on how to dress appropriately for this occasion and weather."""},
            #     # {"type":"text","text":"Below is a person's full wardrobe collection. Tell me details of every clothes."},
            #     {"type":"text", "text": wardrobe},
            # ],
        },
    ],
    max_tokens = 750,
    n = 1
    )

    return response.choices[0].message.content

def wishlist(missing_item,client):
  client = client
  response = client.images.generate(
    model="dall-e-3",
    prompt="You are a fashion advisor. The fashion should be trendy, up-to-date, and aesthetically pleasing. Based on the prompt result below, the guy/girl doesn't have certain clothes that are needed for certain occassion. Make an image of clothes needed, worn by a male model, and the image should not contain any texts or numbers, just model photo." + missing_item,
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
            "content": "You are a fashion advisor. The fashion should be trendy, up-to-date, and aesthetically pleasing. Based on the prompt result below, the guy/girl doesn't have certain clothes that are needed for certain occassion. Describe the missing clothes needed, but the output should not contain accessories." + missing_item
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

# enable = st.checkbox("Enable camera")
# picture = st.camera_input("Take a picture", disabled=not enable)

# if picture is not None:
#     img = Image.open(picture).convert("RGBA")

#     # Convert image to Base64
#     buffered = io.BytesIO()
#     img.save(buffered, format="PNG")  # Ensure it's saved as PNG or other supported format
#     img_base64 = base64.b64encode(buffered.getvalue()).decode()
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image:
#         temp_image.write(base64.b64decode(img_base64))
#         temp_image.flush()

# Display the Streamlit logo
st.image("Logo.png", width=100)

page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url('https://img.freepik.com/free-vector/watercolor-soft-earth-tones-background_23-2151166474.jpg?t=st=1731653114~exp=1731656714~hmac=7145d9393c8d5aa71fa9a385c1b5407f1b33c92cd0a8eb85a4e8d24d5b7c5f82&w=1380');
background-size: cover;

}

[data-testid-"stHeader"]{
background-color: tgba(0,0,0);
}

[data-testid="stToolbar"]{
right: 2rem;
}

[data-testid="stSidebar"]{
background-image: url('https://images.rawpixel.com/image_800/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvcm0yODMtbnVubnktMDMwXzEuanBn.jpg')
}

</style>
"""

st.markdown(page_bg_img,unsafe_allow_html=True)

st.html(
    """
<style>
[data-testid="stSidebarContent"] {
    color: black;
    background-color: white;
}
</style>
"""
)


pg = st.navigation([
    st.Page("pages/Home.py", title="HOME", icon="🏠"),
    st.Page("pages/Wardrobe.py", title="WARDROBE", icon="🚪"),
    st.Page("pages/Wishlist.py", title="WISHLIST", icon="🛍️"),
    st.Page("pages/About Us.py", title="ABOUT US", icon="💁"),
    st.Page("pages/Contact Us.py", title="CUSTOMER SERVICE", icon="🆘"),
])
st.cache_data.clear()
st.cache_resource.clear()
pg.run()

st.cache_data.clear()
st.cache_resource.clear()