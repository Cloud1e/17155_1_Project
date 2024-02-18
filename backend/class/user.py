class User:
    def __init__(self):
        self.__userID = 0
        self.__username = "username"
        self.__password = "password"

    def set_userID(self, userID):
        self.__userID = userID

    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password

    def get_userID(self):
        return self.__userID

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password
