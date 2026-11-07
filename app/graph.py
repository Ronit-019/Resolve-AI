from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

from app.state import ChatState

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


def support_node(state: ChatState):
    response = llm.invoke(state["user_input"])

    return {
        "response": response.content
    }


builder = StateGraph(ChatState)

builder.add_node("support", support_node)

builder.add_edge(START, "support")
builder.add_edge("support", END)

graph = builder.compile()