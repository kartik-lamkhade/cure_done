import os
import urllib.parse
import google.generativeai as genai
from google.generativeai import types
from PIL import Image
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.environ["geminiapi"])
model = genai.GenerativeModel('gemini-2.0-flash')

def analyze_wheat_and_get_link(image):
    # Load your wheat plant photo
    img = image
    # We instruct Gemini to return a clean, predictable text structure
    prompt = """
    Analyze this plant photo. 
    Provide a minimal, brief diagnosis of the disease (maximum 2 sentences).
    Then, provide exactly ONE specific product or chemical control name that directly cures this disease.
    give product name that available mostly in Amazon
    Format your response EXACTLY like this:
    DIAGNOSIS: [Brief info here]
    PRODUCT: [Exact product name here]
    """
    
    # Call the vision model
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
        
        if product_name:
            # Encode the product name for a safe URL (e.g., replaces spaces with %20)
            encoded_query = urllib.parse.quote(product_name)
            
            # Construct a clean, direct Amazon search link for that product
            amazon_link = f"https://www.amazon.com/s?k={encoded_query}"
            
            return {"diagnosis": response_text.split("DIAGNOSIS:")[1].split("PRODUCT:")[0].strip(), "product": product_name, "amazon_link": amazon_link}
            
            # Optional: If you are an Amazon Associate, append your tag to monetize it:
            # affiliate_link = f"{amazon_link}&tag=YOUR_ASSOCIATE_TAG"
            
        else:
            return {"error": "Could not extract product name from Gemini's response."}
            
    except Exception as e:
        return {"error": f"Error building link: {e}"}
