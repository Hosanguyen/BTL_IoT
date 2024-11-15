class User:
    def __init__(self, name, username, password, image1 = '', image2 = '', role = 'user'):
        self.name = name
        self.username = username
        self.password = password
        self.role = role
        self.image1 = image1
        self.image2 = image2

    def to_schema(self):
        return {
            'name': self.name,
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'image1': self.image1,
            'image2': self.image2
        }