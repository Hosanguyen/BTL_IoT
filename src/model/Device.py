class Device:
    def __init__(self, deviceId, topic, alive, mode, status, type):
        self.deviceId = deviceId
        self.topic = topic
        self.alive = alive
        self.mode = mode
        self.status = status
        self.type = type
        
    
    def getStatus(self):
        return self.status
    
    def toSchema(self):
        return {
            'deviceId': self.deviceId,
            'topic': self.topic,
            'alive': self.alive,
            'mode': self.mode,
            'status': self.status,
            'type': self.type
        }