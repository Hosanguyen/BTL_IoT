class Device:
    def __init__(self, name, status, mode, type):
        self.name = name
        self.status = status
        self.mode = mode
        self.type = type
        
    
    def getStatus(self):
        return self.status
    
    def toSchema(self):
        return {
            'name': self.name,
            'status': self.status,
            'mode': self.mode,
            'type': self.type
        }