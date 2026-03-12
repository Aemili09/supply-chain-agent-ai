from fastapi import FastAPI
from pydantic import BaseModel
from agent import agent_executor

app = FastAPI()

class Query(BaseModel):
    text: str
    thread_id: str

@app.post("/chat")
def chat_endpoint(query: Query):
    config = {"configurable": {"thread_id": query.thread_id}}
    response = agent_executor.invoke({"messages": [("user", query.text)]}, config)
    return {"response": response["messages"][-1].content}