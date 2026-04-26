from core.chat import ChatEngine

HELP_TEXT = """
Commands:
  /help             Show this help message
  /persona <name>   Switch persona (default, coder, writer)
  /clear            Reset conversation history
  /cost             Show token usage and cost for the session
  /quit             Exit Prism
"""

DEFAULT_PROVIDER = "OpenAI"
DEFAULT_MODEL = "gpt-4o-mini"

chat = ChatEngine(provider=DEFAULT_PROVIDER, model=DEFAULT_MODEL)

while True:
    user_input = input("\nYOU: ").strip()

    if not user_input:
        continue
    
    if user_input.startswith("/"):
        user_input = user_input.split(maxsplit=1)
        cmd = user_input[0]
        arg = user_input[1] if len(user_input) > 1 else ""

        if cmd == "/help":
            print(HELP_TEXT)
        elif cmd == "/persona":
            if arg:
                chat.change_persona(arg)
            else:
                print("\nUsage: /persona <name>")
        elif cmd == "/clear":
            chat.sliding_window_memory.clear()
        elif cmd == "/cost":
            chat.stats()
        elif cmd == "/quit":
            print("\nGoodbye.")
            break
        else:
            print(f"\nUnknown command: '{cmd}'. Type /help for available commands.")
    else:
        chat.chat(user_input)