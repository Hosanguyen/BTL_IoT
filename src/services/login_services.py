from model.User import User

class LoginService:
    @staticmethod
    def login(username, password):
        """
        Xử lý logic đăng nhập.
        :param username: Tên người dùng
        :param password: Mật khẩu
        :return: dict chứa trạng thái và thông báo
        """
        if not username or not password:
            return {"success": False, "message": "Username and password are required"}

        # Tìm người dùng trong cơ sở dữ liệu
        user = User.find_by_username(username)
        if not user or not user.verify_password(password):
            return {"success": False, "message": "Invalid username or password"}

        return {"success": True, "message": "Login successful"}
