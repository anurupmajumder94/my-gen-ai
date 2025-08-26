from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from dotenv import dotenv_values
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
from langchain_chroma import Chroma
persistent_directory = "db/incidents"
config = dotenv_values(".env")
llm = ChatOpenAI(api_key=config["OPEN_AI_API_KEY"], model="gpt-4o-mini", temperature=0.1)

class AgentState(TypedDict):
   question: str
   context: str
   answer: str

def get_context(agentState: AgentState):
    embeddings = OpenAIEmbeddings(api_key=config["OPEN_AI_API_KEY"], model='text-embedding-3-large')
    db = Chroma(persist_directory=persistent_directory,
                embedding_function=embeddings)
    retriever = db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 3, "score_threshold": 0.7},
    )
    relevant_incidents = retriever.invoke(agentState["question"])
    contexts = []
    for relevant_incident in relevant_incidents:
        contexts.append(
            {
                'description':relevant_incident.metadata['description'],
                'solution':relevant_incident.metadata['solution']
            })
    agentState["context"] = contexts
    return agentState

def generate_answer(agentState: AgentState):
    prompt = f"""
    You are a helpful assistant. Answer the following question from the user.
    Question: {agentState["question"]}

    Your answer must be from the below context only, 
    If you do not find the answer in context mentioned you dont know 
    do not make up answer on your own

    Context: {agentState["context"]}
    """
    agentState["answer"] = llm.invoke(prompt)
    return agentState

workflow = StateGraph(AgentState)
workflow.add_node("RETRIVAL", get_context)
workflow.add_node("GENERATION", generate_answer)

workflow.add_edge(START, "RETRIVAL")
workflow.add_edge("RETRIVAL", "GENERATION")
workflow.add_edge("GENERATION",END)
graph = workflow.compile()

import streamlit as st

# Assuming you already have your graph and AgentState defined somewhere
# from your_module import graph, AgentState

def invoke_graph(question):
    agentState: dict = {
        "question": question,
        "context": "",
        "answer": ""
    }
    agentState = graph.invoke(agentState)
    return agentState["answer"].content

# Streamlit App
st.set_page_config(page_title="LangGraph RAG App", layout="centered")

st.title("🧠 LangGraph Q&A")
st.write("Ask a question and get an answer using your LangGraph pipeline.")

# Input box
question = st.text_input("Enter your question:")

# Button and output
if st.button("Ask"):
    if question.strip():
        with st.spinner("Thinking..."):
            try:
                answer = invoke_graph(question)
                st.success("Answer:")
                st.write(answer)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question.")