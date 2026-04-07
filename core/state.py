class State:
    def __init__(self):
        self.data = {}
        self.progress = {}
        self.history = []

    def update(self, key, value):
        self.data[key] = value
        self.history.append((key, value))

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set_progress(self, task, status):
        self.progress[task] = status

    def get_progress(self):
        return self.progress

    def get_history(self):
        return self.history