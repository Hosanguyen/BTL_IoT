import requests
import json
import time
from datetime import datetime

class SmartDoorAPITest:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.door_id = "Main door"
        self.headers = {
            'Content-Type': 'application/json'
        }

    def log_test(self, test_name, response, expected_status):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "✅ PASSED" if response.status_code == expected_status else "❌ FAILED"
        print(f"\n[{current_time}] Testing: {test_name}")
        print(f"Status: {status}")
        print(f"Expected Status Code: {expected_status}")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 50)

    def test_check_door_status(self):
        """Test GET /api/door endpoint"""
        url = f"{self.base_url}/api/door"
        payload = {
            "door_id": self.door_id
        }
        
        response = requests.get(url, json=payload, headers=self.headers)
        self.log_test("Check Door Status", response, 200)
        return response

    def test_control_door_open(self):
        """Test POST /api/door endpoint - Open Door"""
        url = f"{self.base_url}/api/door"
        payload = {
            "door_id": self.door_id,
            "action": "OPEN"
        }
        
        response = requests.post(url, json=payload, headers=self.headers)
        self.log_test("Control Door - Open", response, 200)
        return response

    def test_control_door_close(self):
        """Test POST /api/door endpoint - Close Door"""
        url = f"{self.base_url}/api/door"
        payload = {
            "door_id": self.door_id,
            "action": "CLOSE"
        }
        
        response = requests.post(url, json=payload, headers=self.headers)
        self.log_test("Control Door - Close", response, 200)
        return response

    def test_control_door_invalid(self):
        """Test POST /api/door endpoint - Invalid Action"""
        url = f"{self.base_url}/api/door"
        payload = {
            "door_id": self.door_id,
            "action": "INVALID"
        }
        
        response = requests.post(url, json=payload, headers=self.headers)
        self.log_test("Control Door - Invalid Action", response, 400)
        return response

    def test_camera_door_open(self):
        """Test POST /api/camera_door endpoint"""
        url = f"{self.base_url}/api/camera_door"
        payload = {
            "door_id": self.door_id
        }
        
        response = requests.post(url, json=payload, headers=self.headers)
        self.log_test("Camera Door Open", response, 200)
        return response

    def run_all_tests(self):
        """Run all API tests in sequence"""
        print("\n🚀 Starting Smart Door API Tests...")
        print("=" * 50)
        
        try:
            # Test 1: Check initial door status
            self.test_check_door_status()
            time.sleep(1)  # Add delay between tests
            
            # Test 2: Open door
            self.test_control_door_open()
            time.sleep(1)
            
            # Test 3: Check door status after opening
            self.test_check_door_status()
            time.sleep(1)
            
            # Test 4: Close door
            self.test_control_door_close()
            time.sleep(1)
            
            # Test 5: Check door status after closing
            self.test_check_door_status()
            time.sleep(1)
            
            # Test 6: Test invalid action
            self.test_control_door_invalid()
            time.sleep(1)
            
            # Test 7: Test camera door open
            self.test_camera_door_open()
            
            print("\n✨ All tests completed!")
            print("=" * 50)
            
        except requests.exceptions.RequestException as e:
            print(f"\n❌ Error running tests: {str(e)}")
            print("=" * 50)

if __name__ == "__main__":
    # Create test instance with your API base URL
    api_test = SmartDoorAPITest(base_url="http://localhost:5000")
    
    # Run all tests
    api_test.run_all_tests()