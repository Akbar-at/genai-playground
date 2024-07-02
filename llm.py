from openai import OpenAI
import streamlit as st


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def generate_response(model,messages):
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    print(st.session_state.messages)
    return stream

def llm_chat(prompt):
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)
    #append chat    
    
    with st.chat_message("assistant"):
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]     
        response = st.write_stream(generate_response(st.session_state["openai_model"],messages))
    return response
