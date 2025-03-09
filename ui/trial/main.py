import streamlit as st

# Create a session state to store user name and exit confirmation
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'exit_confirmation' not in st.session_state:
    st.session_state.exit_confirmation = False

# Streamlit app title
st.title("Welcome to Beta App")

if st.session_state.user_name is None:
    # If user name is not set, display the input form
    user_name = st.text_input("Enter your name:")
    if st.button("Redirect"):
        if user_name:
            st.session_state.user_name = user_name
            st.experimental_rerun()  # Redirect to the new page
        else:
            st.warning("Please enter your name.")
else:
    # User name is set, display the welcome message
    st.title("Welcome to Beta App")
    st.subheader(f"Hello, {st.session_state.user_name}!")

    # Add an "Exit" button
    if st.button("Exit"):
        st.session_state.exit_confirmation = st.warning("Are you sure you want to close the session?")
    
    if st.session_state.exit_confirmation:
        # If the exit confirmation is displayed
        if st.button("Yes"):
            st.session_state.user_name = None  # Reset the session
            st.experimental_rerun()  # Redirect to the name input page
        elif st.button("No"):
            st.session_state.exit_confirmation = False
