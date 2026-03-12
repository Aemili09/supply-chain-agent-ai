from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
from langchain_core.messages import AIMessage

client = TestClient(app)

@patch("main.agent_executor.invoke")
def test_chat_endpoint_health(mock_invoke):
    """Test if the FastAPI chat endpoint is active and returning 200 OK."""
    
    
    mock_msg = AIMessage(content="Hello from the mock AI!")
    msg_list = list()
    msg_list.append(mock_msg)
    
    mock_invoke.return_value = {"messages": msg_list}
    
    response = client.post(
        "/chat",
        json={"text": "Hello", "thread_id": "test_001"}
    )
    assert response.status_code == 200
    assert "response" in response.json()

@patch("main.agent_executor.invoke")
def test_agent_tool_routing(mock_invoke):
    """Test if the agent correctly routes to the supplier tool."""
    
    
    mock_msg = AIMessage(content="Simulated: Found 3 alternative suppliers in Asia.")
    msg_list = list()
    msg_list.append(mock_msg)
    
    mock_invoke.return_value = {"messages": msg_list}
    
    response = client.post(
        "/chat",
        json={"text": "Find alternative suppliers in Asia.", "thread_id": "test_002"}
    )
    assert response.status_code == 200
    assert "3 alternative suppliers" in response.json()["response"]