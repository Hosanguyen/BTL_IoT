class Camera:
    def __init__(self, name, status):
        self.name = name
        self.status = status

    def get_info(self):
        return {
            'name': self.name,
            'status': self.status
        }
