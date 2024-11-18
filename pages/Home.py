from datetime import datetime
import streamlit as st
import main as m
from openai import OpenAI
import json
from dotenv import load_dotenv
import os
import base64
import tempfile
import io
from PIL import Image
load_dotenv()


client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
weatherbit_api_key = os.environ.get('WEATHERBIT_API_KEY')
# Add CSS to center the title and style the buttons and container
st.markdown(
    """
    <style>
    .title {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
    }
    .stButton>button {
        color: black; /* Text color */
        background-color: white; /* Button background color */
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        font-size: 16px;
    }

    /* CSS for the rectangular container around button and expander */
    .rectangular-box {
        padding: 20px;
        background-color: #f0f0f0; /* Box background color */
        border-radius: 8px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); /* Optional shadow */
        text-align: center;
        font-size: 18px;
        margin-bottom: 20px;
        color: black;
    }

    /* Style for the expanded expander background and text color */
    .rectangular-box .st-expander[open] .streamlit-expanderContent {
        background-color: black; /* Background color when expanded */
        color: white; /* Text color when expanded */
        border-radius: 8px;
        padding: 10px;
    }

    /* Change caption color to black */
    .stImage img + figcaption {
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* Import Montserrat font */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

    /* Apply Montserrat font to the entire app */
    body {
        font-family: 'Montserrat', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the title with the custom CSS class
st.markdown('<h1 class="title">Welcome to LookMax.</h1>', unsafe_allow_html=True)

# Use container to group the button and expander together with a rectangular box
with st.container():
    recommendation = None
    # Apply the rectangular box class around the button and expander
    st.markdown('<div class="rectangular-box">', unsafe_allow_html=True)

    # Create two columns for side-by-side layout inside the rectangular box
    col1, col2 = st.columns([1, 1])  # Adjust column widths as needed

    # Place the "Update Wardrobe" button in the first column
    with col1:
        img_base64 = None
        with st.expander("Add to wardrobe"):
            # enable = st.checkbox("Enable camera")
            picture = st.camera_input("Take a picture")
    # Open the image with PIL for processing or saving
            if picture is not None:
                img = Image.open(picture).convert("RGBA")

                # Convert image to Base64
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")  # Ensure it's saved as PNG or other supported format
                img_base64 = base64.b64encode(buffered.getvalue()).decode()
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image:
                    temp_image.write(base64.b64decode(img_base64))
                    temp_image.flush()
            if img_base64 is not None:
                current_fit = m.check_fit(img_base64,client)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"captured_image_{timestamp}.png"
                file_path = os.path.join("./wardrobe_img", filename)
                
                # Save the image to the specified folder
                img.save(file_path)
                m.store_fit(current_fit)
                st.write("Added successfully!")

    # store_fit(current_fit)

    # Place the expander in the second column with input fields
    with col2:
        with st.expander("Give me suggestions"):
            # Add input fields inside the expander
            city = st.text_input("Enter your city for weather-based recommendations:")
            occassion = st.text_input("What's the occasion today?")
            

            # Submit button to process or save the data
            if st.button("Enter"):
                temperature, weather_description = m.get_weather(city, weatherbit_api_key)
    # current_fit = check_fit(img_base64)
    # store_fit(current_fit)
                with open("data.json", 'r') as json_file:
                    data_list = json.load(json_file)
                    dl_asstring = str(data_list)
                    recommendation = m.recommender(dl_asstring, occassion,temperature,weather_description,client)
    if recommendation is not None:
        st.write(recommendation)
        with open('wishlist.json', 'w') as json_file:
            json.dump(recommendation, json_file, indent=4)  

        

    # Close the rectangular box div
    st.markdown('</div>', unsafe_allow_html=True)

