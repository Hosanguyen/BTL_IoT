import datetime
class FireAlarm:
    def __init__(self,deviceId, status, pump_status):
        self.deviceId = deviceId
        # Trạng thái cảm biến lửa (True nếu phát hiện lửa)
        self.status = status
        # Trạng thái máy bơm (True nếu máy bơm đang hoạt động)
        self.pump_status = pump_status
        # Thời gian phát hiện lửa đầu tiên (để lưu trữ thời gian khi phát hiện lửa)
        self.timestamp = datetime.datetime.now()

    def get_info(self):
        return {
            'deviceId': self.deviceId,
            'status': self.status,
            'pump_status': self.pump_status,
            'timestamp': self.timestamp
        }