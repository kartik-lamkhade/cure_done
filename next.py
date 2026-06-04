import os
from fastapi import HTTPException
import urllib.parse
import google.generativeai as genai
from google.generativeai import types
from PIL import Image
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.environ["geminiapi"])
model = genai.GenerativeModel('gemini-1.5-flash-latest')
def analyze_wheat_and_get_link(image):
    img = image
    prompt = """
    Analyze this plant photo. 
    Provide a minimal, brief diagnosis of the disease (maximum 2 sentences).
    Then, provide exactly ONE specific product or chemical control name that directly cures this disease.
    give product name that available mostly in Amazon
    Format your response EXACTLY like this:
    DIAGNOSIS: [Brief info here]
    PRODUCT: [Exact product name here]
    """
    
    response = model.generate_content(
        contents=[img, prompt]
    )
    
    response_text = response.text
    try:
        lines = response_text.strip().split("\n")
        product_name = ""
        for line in lines:
            if line.startswith("PRODUCT:"):
                product_name = line.replace("PRODUCT:", "").strip()
        if not product_name:
            raise HTTPException(status_code=422, detail="Could not extract product name from Gemini's response.")
        if product_name:
            encoded_query = urllib.parse.quote(product_name)
            amazon_link = f"https://www.amazon.com/s?k={encoded_query}"
            return {"diagnosis": response_text.split("DIAGNOSIS:")[1].split("PRODUCT:")[0].strip(), "product": product_name, "amazon_link": amazon_link}
        else:
            raise HTTPException(status_code=400, detail="Could not extract product name from Gemini's response.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error building link: {e}")
