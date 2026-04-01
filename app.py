import streamlit as st
from agent import rag_agent
st.set_page_config(page_title="RAG Agent", layout="wide")

st.title("📚 RAG Agent")


if "messages" not in st.session_state:
    st.session_state.messages = []


query = st.chat_input("Задай вопрос")

if query:

    st.session_state.messages.append({"role": "user", "content": query})


    answer= rag_agent(query)


    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
