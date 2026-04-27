import os
from dotenv import load_dotenv

load_dotenv()

PROVIDERS = {
    "OpenAI":{
        "api_key": os.getenv("OPENAI_API_KEY"),
        "base_url": None,
        "models": {
            "gpt-4o-mini": {
                "input_token_cost": 0.15,
                "output_token_cost": 0.60
            }
        }
    },
    "Groq":{
        "api_key": os.getenv("GROQ_API_KEY"),
        "base_url": os.getenv("GROQ_BASE_URL"),
        "models": {
            "llama-3.1-8b-instant": {
                "input_token_cost": 0.05,
                "output_token_cost": 0.08
            }
        }
    }
}