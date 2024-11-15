import os
import base64
from datetime import datetime
from model.Recognition import Recognition
from pymongo import  DESCENDING
from bson import ObjectId


class RecognitionService:
    def __init__(self, database):
        # Kết nối MongoDB
        self.db = database
        self.recognition_collection = self.db['recognitions']
        
        # Tạo thư mục images trong static
        self.base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        self.images_dir = os.path.join(self.base_dir, 'recognition_images')
        os.makedirs(self.images_dir, exist_ok=True)

    def save_recognition(self, door_id, image_data, user_id):
        try:
            # Tạo tên file dựa trên thời gian
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            image_filename = f"{door_id}_{timestamp}.jpg"
            image_path = os.path.join(self.images_dir, user_id, image_filename)
            if not os.path.exists(os.path.join(self.images_dir, user_id)):
                os.makedirs(os.path.join(self.images_dir, user_id), exist_ok=True)
            # Lưu ảnh
            image_binary = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
            with open(image_path, 'wb') as f:
                f.write(image_binary)

            # Tạo đường dẫn URL cho ảnh
            image_url = f"/static/recognition_images/{user_id}/{image_filename}"

            # Tạo recognition object
            recognition = Recognition(
                door_id=door_id,
                user_id=user_id,
                image_url=image_url,
                timestamp=datetime.now()
            )

            # Lưu vào MongoDB
            result = self.recognition_collection.insert_one(recognition.__dict__)
            recognition._id = result.inserted_id

            return recognition.to_dict()

        except Exception as e:
            print(f"Error saving recognition: {str(e)}")
            raise e

    def get_recognitions(self, door_id=None, limit=10):
        try:
            # Tạo query filter
            query = {'door_id': door_id} if door_id else {}
            
            # Lấy records từ MongoDB
            cursor = self.recognition_collection.find(query)\
                .sort('timestamp', DESCENDING)\
                .limit(limit)
            
            # Chuyển đổi sang list các dict
            records = [Recognition.from_dict(record).to_dict() for record in cursor]
            
            return records
            
        except Exception as e:
            print(f"Error getting recognitions: {str(e)}")
            return []

    def get_recognition_by_id(self, recognition_id):
        try:
            record = self.recognition_collection.find_one({'_id': ObjectId(recognition_id)})
            if record:
                return Recognition.from_dict(record).to_dict()
            return None
        except Exception as e:
            print(f"Error getting recognition by id: {str(e)}")
            return None