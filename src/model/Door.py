class Door:
    def __init__(self, name, status, timestamp, is_open_by_camera=False, is_live=True):
        self.name = name
        self.status = status
        self.timestamp = timestamp
        self.is_open_by_camera = is_open_by_camera
        self.is_live = is_live

    def get_info(self):
        return {
            'name': self.name,
            'status': self.status,
            'timestamp': self.timestamp,
            'is_open_by_camera': self.is_open_by_camera
        }
