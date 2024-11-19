API_ENDPOINT = "https://harshathvenkatesh.us-east-1.aws.modelbit.com/v1/FoodSnap_Prediction_v50/latest"

import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
import base64
import io

st.set_page_config(page_title="Food Snap", page_icon="🍲", layout="wide")

st.title("🍲 Food Snap")
st.markdown("Upload an image to predict the type of Indian food.")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    try:
        image_bytes = uploaded_file.getvalue()
        if not image_bytes:
            st.error("No image data found. Please re-upload the image.")
            st.stop()

        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        payload = {'data': image_base64}

        with st.spinner("Processing..."):
            response = requests.post(API_ENDPOINT, json=payload)

        if response.status_code == 200:
            result = response.json()
            
            data = result.get("data", [])
            if len(data) == 2:
                predicted_label = data[0]
                confidence = data[1]
            else:
                predicted_label = "Unknown"
                confidence = 0

            st.markdown("Prediction Results")
            st.success(f"Predicted Label: {predicted_label}")
            st.info(f"Confidence: {confidence * 100:.2f}%")

        else:
            st.error(f"API Error: {response.status_code}")
            st.text(response.text)
    except UnidentifiedImageError:
        st.error("The uploaded file is not a valid image. Please upload a valid JPG, PNG, or JPEG file.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
