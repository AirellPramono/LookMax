import streamlit as st

st.title("About Us")

# CSS for Montserrat font, rectangular text box, and caption color
st.markdown(
    """
    <style>
    /* Import Montserrat font */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

    /* Apply Montserrat font to the entire app */
    body {
        font-family: 'Montserrat', sans-serif;
    }

    /* CSS for the rectangular text box */
    .text-box {
        padding: 20px;
        background-color: #f0f0f0; /* Box background color */
        border-radius: 8px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); /* Optional shadow */
        text-align: center;
        font-size: 18px;
        margin-bottom: 20px;
        color: black;
    }

    /* Change caption color to black */
    .stImage img + figcaption {
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the rectangular box at the top of the page
st.markdown('<div class="text-box">Welcome to LooksMax - the ultimate wardrobe management app. Our mission is to help you organize and optimize your wardrobe effortlessly, making your daily styling easier and more enjoyable.</div>', unsafe_allow_html=True)

# Add images for the "About Us" section below the text box
st.subheader("Meet the Team")

# Display images in a grid-like layout
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    st.image("ahmad.png", caption="MUHAMMAD AHMAD", width=150)

with col2:
    st.image("arell.png", caption="MUHAMMAD AIRELL", width=150)

with col3:
    st.image("kean.png", caption="CHAN MIN HAN", width=150)

with col4:
    st.image("elijah.png", caption="LAM ZI YONG", width=150)

# Display "Our Vision" section inside a rectangular box
st.subheader("Our Vision")
st.markdown('<div class="text-box">At LooksMax, we envision a world where everyone can easily curate their personal style by effortlessly managing their wardrobe. We strive to make styling accessible and fun, helping you to always feel confident and stylish in your outfits.</div>', unsafe_allow_html=True)
