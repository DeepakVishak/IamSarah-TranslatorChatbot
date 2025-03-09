import streamlit as st

st.title("Echo Bot")

# Initialize chat historty
if "message" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app return
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(messgae["content"])

# React to user input
prompt = st.chat_input("Whats up?")
if prompt :
    #Display user messgae in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user messgae to chat history
    st.session_state.messages.append({"role":"user", "content":prompt})

    response = f"Echo : {prompt}"

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role":"assistant", "content":response})
