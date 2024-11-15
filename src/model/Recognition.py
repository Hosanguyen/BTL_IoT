from datetime import datetime
from bson import ObjectId

class Recognition:
    def __init__(self, door_id, image_url, user_id, timestamp=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.user_id = user_id
        self.door_id = door_id
        self.image_url = image_url
        self.timestamp = timestamp if timestamp else datetime.now()

    @staticmethod
    def from_dict(data):
        return Recognition(
            _id=data.get('_id'),
            user_id=data.get('user_id'),
            door_id=data.get('door_id'),
            image_url=data.get('image_url'),
            timestamp=data.get('timestamp')
        )

    def to_dict(self):
        return {
            '_id': str(self._id),
            'user_id': self.user_id,
            'door_id': self.door_id,
            'image_url': self.image_url,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if isinstance(self.timestamp, datetime) else self.timestamp
        }