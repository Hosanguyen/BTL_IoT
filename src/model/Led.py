class Led():
    def __init__(self, deviceId, status, timestamp):
        self.deviceId = deviceId
        self.status = status
        self.timestamp = timestamp

    def toSchema(self):
        return {
            'deviceId': self.deviceId,
            'status': self.status,
            'timestamp': self.timestamp
        }