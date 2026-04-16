from src.core.exc import Conflict, NotFound

class EmailAlreadyExists(Conflict):
    msg = "Email уже существует"

    def __init__(self):
        super().__init__(detail=self.msg, headers={"x-conflict_field": "email"})

class ProfileIdAlreadyExists(Conflict):
    msg = "Пользователь с таким ID уже существует"

    def __init__(self):
        super().__init__(detail=self.msg, headers={"x-conflict_field": "id"})

class ProfileNotFound(NotFound):
    msg = "Профиль не найден"

    def __init__(self):
        super().__init__(detail=self.msg)
