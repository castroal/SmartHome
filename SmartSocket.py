class SmartSocket(object):
    def __init__(self, id, name, online, state):
        super().__init__()
        self.id = id
        self.name = name
        self.online = online
        self.state = state
        self.ip = None
        self.key = None
        self.version = None
        self.W = None
        self.mA = None
        self.V = None

    def __str__(self):
        return f"Device at {self.ip}: ID {self.id}, state={self.state}, W={self.W}, mA={self.mA}, V={self.V}"