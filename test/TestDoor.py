import requests
import json
import time

class SmartDoorClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.door_endpoint = f"{base_url}/api/door"
        self.camera_endpoint = f"{base_url}/api/camera_door"

    def check_door_status(self, door_name="main_door"):
        """Check the current door status"""
        payload = {
            "door_name": door_name
        }
        try:
            response = requests.get(self.door_endpoint, json=payload)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error checking door status: {e}")
            return None

    def control_door(self, action, door_name):
        """Control door with specified action"""
        payload = {
            "action": action,
            "door_name": door_name
        }
        try:
            response = requests.post(self.door_endpoint, json=payload)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error controlling door: {e}")
            return None

    def camera_door_control(self, door_name):
        """Control door using camera endpoint"""
        payload = {
            "door_name": door_name
        }
        try:
            response = requests.post(self.camera_endpoint, json=payload)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error controlling door with camera: {e}")
            return None

def run_tests():
    client = SmartDoorClient()
    door_name = "main_door"

    print("\n=== Testing Door Status API ===")
    client.check_door_status(door_name)

    print("\n=== Testing Door Control API - Open ===")
    client.control_door("OPEN", door_name)
    time.sleep(1)  # Wait for door status to update
    client.check_door_status(door_name)

    print("\n=== Testing Door Control API - Close ===")
    client.control_door("CLOSE", door_name)
    time.sleep(1)  # Wait for door status to update
    client.check_door_status(door_name)

    print("\n=== Testing Invalid Action ===")
    client.control_door("INVALID", door_name)

    print("\n=== Testing Camera Door Control ===")
    client.camera_door_control(door_name)
    time.sleep(1)  # Wait for door status to update
    client.check_door_status(door_name)

if __name__ == "__main__":
    run_tests()