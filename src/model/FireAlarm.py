import datetime
class FireAlarm:
    def __init__(self, sensor_status=False, pump_status=False, siren_status=False):
        # Trạng thái cảm biến lửa (True nếu phát hiện lửa)
        self.sensor_status = sensor_status
        # Trạng thái máy bơm (True nếu máy bơm đang hoạt động)
        self.pump_status = pump_status
        # Trạng thái còi (True nếu còi đang kêu)
        self.siren_status = siren_status
        # Thời gian phát hiện lửa đầu tiên (để lưu trữ thời gian khi phát hiện lửa)
        self.timestamp = datetime.datetime.now()

    def get_info(self):
        return {
            'sensor_status': self.sensor_status,
            'pump_status': self.pump_status,
            'siren_status': self.siren_status,
            'timestamp': self.timestamp
        }