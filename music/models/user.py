from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id, email, username, password, usersongs):
        self.id = id
        self.email = email
        self.username = username
        self.password = password
        self.usersongs = usersongs
