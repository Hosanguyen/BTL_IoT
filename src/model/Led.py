class Led():
    def __init__(self, name, status, timestamp):
        self.name = name
        self.status = status
        self.timestamp = timestamp

    def toSchema(self):
        return {
            'name': self.name,
            'status': self.status,
            'timestamp': self.timestamp
        }