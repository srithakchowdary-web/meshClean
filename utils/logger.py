class Logger:
    def __init__(self):
        self.logs = []

    def log(self, msg):
        self.logs.append(msg)

    def get_logs(self):
        return "\n".join(self.logs)