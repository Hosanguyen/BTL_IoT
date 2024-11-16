from flask import Blueprint, request, jsonify
from model.User import User
from services.user_services import add_user,check_user,get_users,get_user,update_user,update_image,delete_user

userAPI = Blueprint('userAPI', __name__)
@userAPI.route('/api/user/signup', methods=['POST'])
def signup():
    data = request.json
    user = User(username=data.get('username'),password=data.get('password'), name=data.get('name'),role=data.get('role'))
    if add_user(user):
        return jsonify({'status': 'Tạo tài khoản thành công'}), 200
    else:
        return jsonify({'error': 'Username đã tồn tại'}), 400

@userAPI.route('/api/user/login', methods=['POST'])
def login():
    data = request.json
    result = check_user(data.get('username'), data.get('password'))
    if result:
        return jsonify({'status':'Đăng nhập thành công','data': result}), 200
    else:
        return jsonify({'error': 'Sai tài khoản hoặc mật khẩu'}), 400
    
@userAPI.route('/api/user/getusers', methods=['GET'])
def getusers():
    return jsonify({'listUser': get_users()}), 200

@userAPI.route('/api/user/detailuser', methods=['GET'])
def getuser():
    _id = request.args.get('_id')
    return jsonify({'user': get_user(_id)}), 200

@userAPI.route('/api/user/updateuser', methods=['PUT'])
def updateUser():
    data = request.json
    _id = data.get('_id')
    name = data.get('name')
    password = data.get('password')
    update_user(_id, name, password)
    return jsonify({'status': 'Cập nhật thành công'}), 200

@userAPI.route('/api/user/updateimage', methods=['PUT'])
def updateImageUser():
    data = request.json
    _id = data.get('_id')
    image1 = data.get('image1')
    image2 = data.get('image2')
    update_image(_id, image1, image2)
    return jsonify({'status': 'Cập nhật ảnh thành công'}), 200

@userAPI.route('/api/user/delete', methods=['DELETE'])
def deleteUser():
    _id = request.args.get('_id')
    delete_user(_id)
    return jsonify({'status': 'Xóa thành công'}), 200