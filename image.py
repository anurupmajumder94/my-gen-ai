import base64
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

image_base64 = encode_image("rust.png")

message = HumanMessage(
    content=[
        {"type": "text", "text": "What is in this picture?"},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
    ]
)

from dotenv import dotenv_values
config = dotenv_values(".env")

llm = ChatOpenAI(api_key=config["OPEN_AI_API_KEY"], model="gpt-4o-mini", temperature=0.1)

response = llm.invoke([message])
print(response.content)
