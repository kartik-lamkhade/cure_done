import requests
import streamlit as st

st.title("Plant Disease Analyzer")
st.write("Upload a photo of your plant to get a diagnosis and treatment recommendation.")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"])
if uploaded_file is not None:
    st.image(uploaded_file, caption='Uploaded Image')
    
    # Here you would call your backend API to analyze the image and get the response
    # For demonstration, we'll just show a placeholder response
    with st.spinner("Analyzing the image..."):
        response = requests.post("https://cure-done.onrender.com/analyze-wheat",files={"Upload_file": (uploaded_file.name, uploaded_file, "image/jpeg")})
    st.write(f"**diagnosis:** {response.json()['diagnosis']}")
    st.write(f"**product:** {response.json()['product']}")
    st.write(f"**amazon_link:** {response.json()['amazon_link']}")
