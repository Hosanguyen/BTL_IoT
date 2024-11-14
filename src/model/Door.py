class Door:
    def __init__(self, deviceId, status, timestamp, is_open_by_camera=False, is_live=True):
        self.deviceId = deviceId
        self.status = status
        self.timestamp = timestamp
        self.is_open_by_camera = is_open_by_camera
        self.is_live = is_live

    def get_info(self):
        return {
            'deviceId': self.deviceId,
            'status': self.status,
            'timestamp': self.timestamp,
            'is_open_by_camera': self.is_open_by_camera
        }
