import os
import base64
from groq import Groq

# Step 1: Setup Groq API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Step 2: Convert Image to required text
# image_path = "acene_img.jpg"

def encode_image(image_path):
    image_path = "acene_img.jpg"
    with open(image_path, "rb") as image_file:
       return base64.b64encode(image_file.read()).decode('utf-8')

# Step 3: Setup multimodal LLM
query = "is there something wrong"
model = "meta-llama/llama-4-scout-17b-16e-instruct"
def analyze_image_with_query(query,model,encoded_image):

    client = Groq(api_key=GROQ_API_KEY)
   
    


    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpg;base64,{encoded_image}",
                    },
                },
            ],
        }
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
    )

    return chat_completion.choices[0].message.content
