import config
from providers import ask_gemini, ask_ollama, ask_openai

HELP = """
Commands:
  /help   Show this help
  /exit   Quit the chatbot (you can also type: exit)
"""


def model_name():
    """The model name of the provider that was chosen in .env."""
    if config.PROVIDER == "openai":
        return config.OPENAI_MODEL
    if config.PROVIDER == "gemini":
        return config.GEMINI_MODEL
    if config.PROVIDER == "ollama":
        return config.OLLAMA_MODEL


def check_setup():
    """Return a helpful message if something is missing in .env, otherwise None."""
    if config.PROVIDER not in ("openai", "gemini", "ollama"):
        return (
            "LLM_PROVIDER is '" + config.PROVIDER + "'.\n"
            "Please set LLM_PROVIDER to openai, gemini or ollama in the .env file."
        )
    if config.PROVIDER == "openai" and not config.OPENAI_API_KEY:
        return "OPENAI_API_KEY is missing.\nPlease add your OpenAI API key to the .env file."
    if config.PROVIDER == "gemini" and not config.GEMINI_API_KEY:
        return "GEMINI_API_KEY is missing.\nPlease add your Gemini API key to the .env file."
    if not model_name():
        return (
            "The model name for " + config.PROVIDER + " is missing.\n"
            "Please set " + config.PROVIDER.upper() + "_MODEL in the .env file."
        )


def ask_llm(message):
    """Send the message to whichever provider was chosen in .env."""
    if config.PROVIDER == "openai":
        return ask_openai(message)
    elif config.PROVIDER == "gemini":
        return ask_gemini(message)
    else:
        return ask_ollama(message)


def main():
    problem = check_setup()
    if problem:
        print("Error:", problem)
        return

    print("=" * 40)
    print("      Simple GenAI CLI Chatbot")
    print("=" * 40)
    print("\nProvider:", config.PROVIDER)
    print("Model:", model_name())
    print("Type /help for commands.")

    while True:
        #while true so that the chatbot contines unless u quit
        message = input("\nYou: ").strip()
        #you means ur mesage

        if message in ("exit", "/exit"):
            print("\nGoodbye!")
            break

        if message == "/help":
            print(HELP)
            continue

        if not message:
            #no question has been asked and enter is pressed
            continue

        try:
            print("\nAssistant:", ask_llm(message))
        except Exception as error:
            print("\nSorry, the request failed:", error)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
