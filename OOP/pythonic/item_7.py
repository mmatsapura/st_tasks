class Server:
    def __init__(self, processes):
        self.processes = processes

    def __getitem__(self, key):
        return self.processes[key]

    def __setitem__(self, key, value):
        self.processes[key] = value


s = Server({"nginx": "running", "db": "stopped"})
print(s["nginx"])  # running
s["db"] = "running"
print(s["db"])     # running