import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
import time

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        response = model.generate_content([input, image[0], prompt])
        return response.text
    except Exception as e:
        st.error(f"Error during API call: {e}")
        return None

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return [{"mime_type": uploaded_file.type, "data": bytes_data}]
    else:
        st.error("No file uploaded")
        return None

input_prompt = """
You are an expert pharmaceutical/chemist...
"""

st.set_page_config(page_title="AI Chemist App")
st.header("AI Chemist App")

input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

if st.button("Tell me"):
    image_data = input_image_setup(uploaded_file)
    if image_data:
        with st.spinner('Generating response...'):
            response = get_gemini_response(input_prompt, image_data, input_text)
            if response:
                st.subheader("The Response is")
                st.write(response)
