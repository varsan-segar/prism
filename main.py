from core.chat import ChatEngine

DEFAULT_PROVIDER = "OpenAI"
DEFAULT_MODEL = "gpt-4o-mini"

chat = ChatEngine(provider=DEFAULT_PROVIDER, model=DEFAULT_MODEL)


while True:
    user_input = input("\nYOU: ").strip()

    if not user_input:
        continue

    if user_input.lower() == "/quit":
        print("\n Goodbye.")
        break
    
    if user_input.startswith("/"):
        user_input = user_input.split(maxsplit=1)
        cmd = user_input[0]
        arg = user_input[1] if len(user_input) > 1 else ""
        
        if cmd == "/persona":
            chat.change_persona(arg)
        
        if cmd == "/cost":
            chat.stats()
    else:
        chat.chat(user_input)