class SlidingWindowMemory:
    def __init__(self, max_turns):
        self.turns = 0
        self.max_messages = max_turns * 2
        self.message = []

    def add(self, role, message):
        self.message.append({"role": role, "content": message})

        if role == "assistant":
            self.turns += 1

    def get_messages(self):
        return self.message
    
    def clear(self):
        self.message.clear()
    
    def sliding_window(self):
        if len(self.message) > self.max_messages:
            self.message = self.message[-self.max_messages:]