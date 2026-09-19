class Server:
    def __init__(self, name):
        self.name = name

    def __call__(self, action):
        return f"{self.name} execute {action}"


s = Server("Web")
print(s("restart"))  # Web execute restart

# call server as function
