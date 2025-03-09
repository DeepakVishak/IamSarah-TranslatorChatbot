import openai

# Set your OpenAI API key
api_key = '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'

def chat_with_gpt3(prompt):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text

if __name__ == "__main__":
    print("Chatbot: Hello! How can I assist you today?")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        # Include user input as a prompt for GPT-3
        prompt = f"User: {user_input}\nChatbot:"
        response = chat_with_gpt3(prompt)
        print("Chatbot:", response)
