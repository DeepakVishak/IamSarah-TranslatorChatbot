import streamlit as st

# Create a function for the homepage
def homepage():
    st.title("Welcome to the Streamlit Multi-Page App")
    st.write("This is the homepage of the app.")
    st.write("Use the sidebar to navigate to the application page.")

# Create a function for the application page
def application():
    st.title("Application Page")
    st.write("This is the application page of the app.")
    st.write("You can add your application content here.")

# Create buttons for navigation
page = st.button("Homepage")
if page:
    homepage()

page = st.button("Application")
if page:
    application()
