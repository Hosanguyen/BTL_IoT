class User:
    def __init__(self, name, username, password, image1 = '', image2 = '', role = 'user', idImage1 = '', idImage2 = ''):
        self.name = name
        self.username = username
        self.password = password
        self.role = role
        self.image1 = image1
        self.image2 = image2
        self.idImage1 = idImage1
        self.idImage2 = idImage2

    def to_schema(self):
        return {
            'name': self.name,
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'image1': self.image1,
            'image2': self.image2,
            'idImage1': self.idImage1,
            'idImage2': self.idImage2
        }