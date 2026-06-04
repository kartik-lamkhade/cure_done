import os
from fastapi import HTTPException
import urllib.parse
import base64
import io
from openai import OpenAI
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["geminiapi"],
)

def analyze_wheat_and_get_link(image):
    # Convert PIL image to base64 for OpenRouter
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    b64 = base64.b64encode(buffer.getvalue()).decode()

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
    response = client.chat.completions.create(
        model="google/gemini-2.0-flash-exp:free",
        messages=[{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
            {"type": "text", "text": prompt}
        ]}]
    )

    response_text = response.choices[0].message.content

    try:
        lines = response_text.strip().split("\n")
        product_name = ""
        for line in lines:
            if line.startswith("PRODUCT:"):
                product_name = line.replace("PRODUCT:", "").strip()
        if not product_name:
            raise HTTPException(status_code=422, detail="Could not extract product name from response.")
        if product_name:
            encoded_query = urllib.parse.quote(product_name)
            amazon_link = f"https://www.amazon.com/s?k={encoded_query}"
            return {"diagnosis": response_text.split("DIAGNOSIS:")[1].split("PRODUCT:")[0].strip(), "product": product_name, "amazon_link": amazon_link}
        else:
            raise HTTPException(status_code=400, detail="Could not extract product name from response.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error building link: {e}")
