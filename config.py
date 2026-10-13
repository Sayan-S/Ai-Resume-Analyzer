import os

from dotenv import load_dotenv

# Reads the .env file and puts its values into the environment,
# so we never have to hard-code secrets inside our Python files.
load_dotenv()


PROVIDER = os.getenv("LLM_PROVIDER", "openai") # , "openai" is the default value if LLM_PROVIDER fails
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful AI assistant.") #same default value

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL","gpt-4o-mini")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
