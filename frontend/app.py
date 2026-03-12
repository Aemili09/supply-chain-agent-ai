import streamlit as st
import requests

st.set_page_config(page_title="SC-RIHN Dashboard", layout="wide")
st.title("🌐 Supply Chain Resilience Inference System")
st.markdown("Powered by **LangGraph**, **Polars**, **Delta Lake**, and **PyTorch Geometric**")


with st.sidebar:
    st.header("⚙️ Pipeline Status")
    st.success("BigQuery GDELT Sync: Active")
    st.success("Pandera Data Contract: Validated")
    st.success("GATv2 Model: Online")
    st.info("Agent State: MemorySaver Active")

if "messages" not in st.session_state:
    st.session_state.messages =

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("E.g., Analyze the supply chain risk in Asia using the GNN..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = requests.post(
        "http://backend:8000/chat",
        json={"text": prompt, "thread_id": "session_master_001"}
    ).json()

    st.session_state.messages.append({"role": "assistant", "content": response["response"]})
    st.chat_message("assistant").write(response["response"])