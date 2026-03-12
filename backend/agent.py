import os
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langfuse.langchain import CallbackHandler


langfuse_handler = CallbackHandler()


@tool
def predict_supply_chain_risk(region: str) -> str:
    """Run the GATv2 Graph Neural Network to predict supply chain risk for a region."""
    
    return f"GNN Inference Complete: High disruption probability detected in {region} due to maritime congestion."

@tool
def search_alternative_suppliers(region: str) -> str:
    """Search the enterprise Delta Lake for alternative suppliers in a specific region."""
    return f"Delta Lake Query: Found 3 verified alternative suppliers in {region}."


class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatOpenAI(model="gpt-4o").bind_tools([predict_supply_chain_risk, search_alternative_suppliers])


def chatbot(state: State):
    
    return {"messages": [llm.invoke(state["messages"], config={"callbacks": [langfuse_handler]})]}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

memory = MemorySaver()
agent_executor = graph_builder.compile(checkpointer=memory)