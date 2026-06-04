from fastapi import FastAPI,UploadFile, File
from PIL import Image
import io
from main.next import analyze_wheat_and_get_link
app = FastAPI()
@app.get("/")
def home():
    return {"message": "Welcome to the Wheat Disease Analyzer API! To analyze a wheat plant photo, send a GET request to /analyze-wheat with the image path as a query parameter. For example: /analyze-wheat?image_path=path/to/your/wheat_photo.jpg"}
@app.post("/analyze-wheat")
def analyze_wheat(Upload_file: UploadFile = File(...)):
    image_bytes = Upload_file.file.read()
    img = Image.open(io.BytesIO(image_bytes))
    return analyze_wheat_and_get_link(img)
