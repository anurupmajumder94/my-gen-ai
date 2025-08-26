from langchain_openai import ChatOpenAI
from dotenv import dotenv_values
config = dotenv_values(".env")

llm = ChatOpenAI(api_key=config["OPEN_AI_API_KEY"], model="gpt-4o-mini", temperature=0.1)
response = llm.invoke("Who is the President of India?")
print(response.content)