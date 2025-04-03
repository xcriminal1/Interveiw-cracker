import os

MODE = os.getenv("MODE", "gui")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set your OPENAI_API_KEY in the environment or in the .env file.")
