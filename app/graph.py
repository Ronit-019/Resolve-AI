from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode, tools_condition

from app.state import ChatState
from app.tools import get_order_details

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

SYSTEM_PROMPT = """
You are Resolve, a generic AI-powered customer support agent
specializing in order management.

Your responsibilities:
- Assist customers with order-related questions and issues.
- Help with order status, delivery tracking, delays, cancellations,
  returns and refunds.
- Ask relevant questions to understand customer problems.
- Guide customers through appropriate resolution processes.

Your behaviour:
- Be professional, empathetic, concise and solution-oriented.
- Use clear, simple language.
- Acknowledge customer frustration when appropriate.
- Ask one relevant question at a time.
- Avoid unnecessary explanations and repetitive questions.

Your boundaries:
- Never invent order details, delivery updates, policies or refund information.
- Never claim an action has been completed unless successfully executed.
- Never promise outcomes you cannot guarantee.
- Stay focused on customer support and order management.
- If information is unavailable, communicate that honestly.
- For order-specific queries, use get_order_details whenever an order ID is available.
- If the customer hasn't provided an order ID, ask for it.
- Never assume an order ID from previous conversation messages.
- Only share information returned by the database.
- Never invent tracking links, delivery estimates, shipping timelines, or carrier updates.
- Do not claim to arrange follow-ups or perform actions that are not supported by tools.
"""

tools = [get_order_details]

llm_with_tools = llm.bind_tools(tools)

def support_node(state: ChatState):
    messages = [
        ("system", SYSTEM_PROMPT),
        *state["messages"]
    ]

    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}


builder = StateGraph(ChatState)

builder.add_node("support", support_node)

builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "support")

builder.add_conditional_edges("support", tools_condition)

builder.add_edge("tools", "support")

memory = InMemorySaver()

graph = builder.compile(checkpointer=memory)