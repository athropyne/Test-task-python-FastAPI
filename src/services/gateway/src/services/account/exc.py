from src.core.exc import Conflict, ClientError

class UsernameAlreadyExists(Conflict):
    msg = "Имя пользователя уже существует"
    def __init__(self):
        super().__init__(detail=self.msg)

class InvalidUserOrPassword(ClientError):
    msg = "Неверное имя пользователя или пароль"
    def __init__(self):
        super().__init__(detail=self.msg)