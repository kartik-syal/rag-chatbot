import streamlit as st
import requests

st.title("RAG ChatBot")

query = st.text_area("Enter your query:")
if st.button("Submit"):
    response = requests.post("http://localhost:8000/api/query", json={"query": query})
    if response.status_code == 200:
        data = response.json()
        st.write("### Answer")
        st.write(data["answer"])
        # st.write("### Context")
        # for context in data["context"]:
        #     st.write(context)
    else:
        st.write("Error:", response.status_code, response.text)
