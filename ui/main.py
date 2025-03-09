import streamlit as st

# Define correct credentials (you can replace these with your own)
correct_username = "user"
correct_password = "password"

# Create a session state to store user login status and last activity time
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.last_activity_time = None

# Streamlit app title
st.title("Login Page")

# JavaScript code for inactivity timeout and session timeout popup (as shown in the previous response)
js_code = """
<script>
    const idleTimeout = 10 * 1000; // 10 seconds in milliseconds
    let timeout;

    function resetTimeout() {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            alert("Session Timeout");
            window.location.reload();  // Refresh the page to go back to the login page
        }, idleTimeout);
    }

    // Detect user activity and reset the timeout
    document.addEventListener("mousemove", resetTimeout);
    document.addEventListener("keydown", resetTimeout);

    // Initialize the timeout
    resetTimeout();
</script>
"""

# Display the JavaScript code
st.write(js_code, unsafe_allow_html=True)

if st.session_state.user is None:
    # Create input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Create a submit button
    if st.button("Submit"):
        if username == correct_username and password == correct_password:
            st.success("Login Successful!")
            st.session_state.user = username  # Store the user in session state
            st.session_state.last_activity_time = st.session_info.script_request_time  # Record the last activity time
        else:
            st.error("Incorrect credentials. Please try again.")

    # Add options for creating an account, forgot username, and forgot password
    st.write("Options:")
    if st.button("Create an Account"):
        st.warning("Coming soon in development")
    
    if st.button("Forgot Username"):
        st.warning("Coming soon in development")

    if st.button("Forgot Password"):
        st.warning("Coming soon in development")
else:
    # User is logged in, display the "Welcome to beta app" page
    st.title("Welcome to beta app")
    st.write(f"Hello, {st.session_state.user}!")

    # You can add more content and functionality for the logged-in user here.
