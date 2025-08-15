print("Hello! I'm ChatBot Flash. Type 'bye' to exit.")

while True:
    user_input = input("You: ").lower()

    if user_input == "hello":
        print("Faslh: Hi there! How can I help you?")
    elif user_input == "how are you":
        print("Flash: I'm just a bunch of code, but I'm doing great! 😄")
    elif user_input == "what is your name":
        print("Flash: I'm Flash, your friendly assistant.")
    elif user_input == "bye":
        print("Flash: Goodbye! Have a great day! 👋")
        break
    else:
        print("Flash: Sorry, I didn't understand that. Can you try something else?")
