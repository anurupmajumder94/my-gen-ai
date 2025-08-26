"""
Input: Country Name
Output: A full sentence mention Capital of the country
"""

from langchain_openai import ChatOpenAI
from dotenv import dotenv_values
config = dotenv_values(".env")

def interact_llm(country_name):
    promt = f"""
    What is the Capital of {country_name} ?
    """
    llm = ChatOpenAI(api_key=config["OPEN_AI_API_KEY"], model="gpt-4o-mini", temperature=0.1)
    response = llm.invoke(promt)
    return response.content


response = interact_llm("India")
print(response)