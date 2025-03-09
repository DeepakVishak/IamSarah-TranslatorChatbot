import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Get the list of available voices
voices = engine.getProperty('voices')

# Find the Malayalam voice
malayalam_voice = None
for voice in voices:
    if "malayalam" in voice.languages:
        malayalam_voice = voice
        break

# Set the voice to the Malayalam voice, if found
if malayalam_voice:
    engine.setProperty('voice', malayalam_voice.id)
else:
    print("Malayalam voice not found. Using the default voice.")

# Malayalam phrase you want to say
malayalam_text = "എല്ലാം നന്നായി നടക്കുമെന്ന് ഞാൻ പ്രതീക്ഷിക്കുന്നു"

# Use the engine to say the phrase
engine.say(malayalam_text)

# Wait for the speech to finish
engine.runAndWait()

# Close the engine
engine.stop()
