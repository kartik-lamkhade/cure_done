import requests
import streamlit as st

st.title("Plant Disease Analyzer")
st.write("Upload a photo of your plant to get a diagnosis and treatment recommendation.")
uploaded_file = st.camera_input("Take a picture")
if uploaded_file is not None:
    with st.spinner("Analyzing the image..."):
        response = requests.post("https://cure-done.onrender.com/analyze-wheat",files={"Upload_file": (uploaded_file.name, uploaded_file, "image/jpeg")})
    try: 
        st.write(f"**diagnosis:** {response.json()['diagnosis']}")
        st.write(f"**product:** {response.json()['product']}")
        st.write(f"**amazon_link:** {response.json()['amazon_link']}")
    except Exception as e:
        st.error("An error occurred while processing the image. Please try again./n may be api limit over")
        st.error(str(e))
