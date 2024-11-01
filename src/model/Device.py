class Device:
    def __init__(self, name, status, type):
        self.name = name
        self.status = status
        self.type = type
    
    def getStatus(self):
        return self.status
    
    def toSchema(self):
        return {
            'name': self.name,
            'status': self.status,
            'type': self.type
        }