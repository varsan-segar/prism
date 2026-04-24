from config import PROVIDERS

class CostTracker():
    def __init__(self, provider, model):
        self.provider = provider
        self.model = model
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.usd_to_inr = 94
        self.history = []
    
    def add(self, input_tokens, output_tokens):
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
    
    def calculate_cost(self):
        pricing = PROVIDERS[self.provider]["models"][self.model]

        total_input_tokens_cost_usd = self.total_input_tokens * ((pricing["input_token_cost"]) / 1_000_000)
        total_output_tokens_cost_usd = self.total_output_tokens * ((pricing["output_token_cost"]) / 1_000_000)

        total_cost_usd = total_input_tokens_cost_usd + total_output_tokens_cost_usd

        return total_input_tokens_cost_usd, total_output_tokens_cost_usd, total_cost_usd

    def change_provider(self, provider, model):
        total_input_tokens_cost_usd, total_output_tokens_cost_usd, total_cost_usd = self.calculate_cost()

        if self.total_input_tokens > 0 or self.total_output_tokens > 0:
            self.history.append({
                "provider": self.provider,
                "model": self.model,
                "total_input_tokens": self.total_input_tokens,
                "total_output_tokens": self.total_output_tokens,
                "total_input_tokens_cost_usd": total_input_tokens_cost_usd,
                "total_output_tokens_cost_usd": total_output_tokens_cost_usd,
                "total_cost_usd": total_cost_usd
            })

        self.provider = provider
        self.model = model
        self.total_input_tokens = 0
        self.total_output_tokens = 0
    
    def summary(self):
        if self.history:
            for segment in self.history:
                print("\n--- Segment ---")
                print(f"Provider: {segment['provider']}")
                print(f"Model: {segment['model']}")
                print(f"Input/Output Tokens: {segment['total_input_tokens']}/{segment['total_output_tokens']}")
                print(f"Input Tokens Cost (USD/INR): {segment['total_input_tokens_cost_usd']:.6f}/{(segment['total_input_tokens_cost_usd'] * self.usd_to_inr):.6f}")
                print(f"Output Tokens Cost (USD/INR): {segment['total_output_tokens_cost_usd']:.6f}/{(segment['total_output_tokens_cost_usd'] * self.usd_to_inr):.6f}")
                print(f"Total Session Cost (USD/INR): {segment['total_cost_usd']:.4f}/{(segment['total_cost_usd'] * self.usd_to_inr):.4f}")

        total_input_tokens_cost_usd, total_output_tokens_cost_usd, total_cost_usd = self.calculate_cost()

        print("\n--- Segment ---")
        print(f"Provider: {self.provider}")
        print(f"Model: {self.model}")
        print(f"Input/Output Tokens: {self.total_input_tokens}/{self.total_output_tokens}")
        print(f"Input Tokens Cost (USD/INR): {total_input_tokens_cost_usd:.6f}/{(total_input_tokens_cost_usd * self.usd_to_inr):.6f}")
        print(f"Output Tokens Cost (USD/INR): {total_output_tokens_cost_usd:.6f}/{(total_output_tokens_cost_usd * self.usd_to_inr):.6f}")
        print(f"Total Session Cost (USD/INR): {total_cost_usd:.4f}/{(total_cost_usd * self.usd_to_inr):.4f}")