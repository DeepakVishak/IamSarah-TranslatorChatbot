"""
import streamlit as st

instr = 'Hi there! Enter what you want to let me know here.'

# Create two columns; adjust the ratio to your liking
col1, col2 = st.columns([9, 1])

# Use the first column for text input
with col1:
    prompt = st.text_input("")

# Use the second column for the submit button
with col2:
    # Use a dynamic label for the submit button based on whether the prompt is empty or not
    submitted = st.button('Speech' if not prompt else 'Chat')

if prompt and submitted:
    # Do something with the inputted text here
    st.write(f"You said: {prompt}")
"""

import streamlit as st
from datetime import datetime
import time


# Section 1
button = st.button('Button')
button_placeholder = st.empty()
button_placeholder.write(f'button = {button}')
time.sleep(2)
button = False
button_placeholder.write(f'button = {button}')

# Section 2
time_placeholder = st.empty()

while True:
    timenow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_placeholder.write(timenow)
    time.sleep(1)