class SlidingWindowMemory:
    def __init__(self, max_turns):
        self.total_turns = 0
        self.dropped_turns = 0
        self.max_messages = max_turns * 2
        self.messages = []

    def add(self, role, content):
        self.messages.append({"role": role, "content": content})

        if role == "assistant":
            self.total_turns += 1
    
    def sliding_window(self):
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
            self.dropped_turns += 1

    def get_messages(self):
        return self.messages
    
    def clear(self):
        self.messages.clear()