import streamlit as st
from AuthenticationComponents import login  
from AuthenticationComponents import createaccount
from AuthenticationComponents import forgetuidpassword

st.set_page_config(
    page_title="Multipage App",
    page_icon="👋",
)

# Create a sidebar with navigation options
page = st.sidebar.selectbox("Select a page", ["Login", "Create Account", "Forget UserID/Password"])

# Display the selected page
if page == "Login":
    login.mainpage()
elif page == "Create Account":
    createaccount.mainpage()
elif page == "Forget UserID/Password":
    forgetuidpassword.mainpage()
