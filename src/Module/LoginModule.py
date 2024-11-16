from flask import Blueprint, request, jsonify
from services.user_services import check_user  # Import hàm kiểm tra người dùng từ user_services

# Tạo Blueprint cho LoginModule
login_module = Blueprint('login', __name__)

@login_module.route('/api/login', methods=['POST'])
def login():
    """
    Route để xử lý đăng nhập.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')
    print("Received data:", data)  # Kiểm tra dữ liệu gửi từ frontend

    # Kiểm tra xem tên người dùng và mật khẩu có tồn tại và hợp lệ không
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    # Sử dụng dịch vụ để xác thực người dùng
    user = check_user(username, password)

    if user:
        return jsonify({"message": "Login successful", "user": user}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401
