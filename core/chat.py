import json
import time
from pathlib import Path
from openai import (
    OpenAI,
    AuthenticationError,
    BadRequestError,
    APIConnectionError,
    APITimeoutError,
    RateLimitError
)
from config import PROVIDERS
from .cost import CostTracker
from .memory import SlidingWindowMemory

class ChatEngine:
    def __init__(self, provider, model):
        self.provider = provider
        self.model = model
        self.current_persona = "default"
        self.system_promt = self.load_persona(persona=self.current_persona)
        self.sliding_window_memory = SlidingWindowMemory(max_turns=10)
        self.cost_tracker = CostTracker(self.provider, self.model)
    
    def api_request(self, history, max_retries=3):
        for attempt in range(max_retries):
            try:
                client = OpenAI(api_key=PROVIDERS[self.provider]["api_key"], base_url=PROVIDERS[self.provider]["base_url"])

                stream = client.chat.completions.create(
                    model=self.model,
                    messages=history,
                    temperature=0.7,
                    stream=True,
                    stream_options={"include_usage": True}
                )

                print("\nAI: ", end="", flush=True)

                response = ""

                for chunk in stream:
                    if not chunk.choices:
                        if hasattr(chunk, "usage") and chunk.usage:
                            self.cost_tracker.add(input_tokens=chunk.usage.prompt_tokens, output_tokens=chunk.usage.completion_tokens)
                        
                        continue
                    
                    delta = chunk.choices[0].delta
                    content = getattr(delta, "content", None)

                    if content:
                        print(content, end="", flush=True)
                        response += content
                print()

                return response
            except AuthenticationError:
                print("Authentication Error. Check API KEY")
                break
            except BadRequestError as e:
                print(f"Bad Request Error -> {e}")
                break
            except APIConnectionError:
                print("API Connection Error. Trying again.")
                time.sleep(1)
            except APITimeoutError:
                print("API Timeout Error. Trying again.")
                time.sleep(2)
            except RateLimitError:
                wait = attempt ** 2
                print(f"Rate Limited. Wait for {wait}s and try again.")
                time.sleep(wait)
        
        print("All retry attempt failed")
        history = history.pop()

        return history
    
    def load_persona(self, persona):
        path = Path("personas") / f"{persona}.json"

        if not path.exists():
            print("\nPath not exixts. Switching to default persona.")
            return self.system_promt

        with open(path) as f:
            data = json.load(f)
        
        return data["system_prompt"]

    def change_persona(self, persona):
        self.system_promt = self.load_persona(persona=persona)
        self.current_persona = persona
        print(f"\n[Persona switched to {persona}]")

    def chat(self, user_message):
        self.sliding_window_memory.add("user", user_message)

        history = [
            {
                "role": "system",
                "content": self.system_promt
            },
            *self.sliding_window_memory.get_messages()
        ]

        assistant = self.api_request(history=history)

        self.sliding_window_memory.add("assistant", assistant)
    
    def stats(self):
        print("---Session Summary---")
        print(f"Total Turns: {self.sliding_window_memory.turns}")
        self.cost_tracker.summary()