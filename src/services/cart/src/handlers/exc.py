from src.core.exc import NotFound, Conflict

class ProductNotFound(NotFound):
    msg = "Продукт с таким ID отсутствует в корзине"

    def __init__(self):
        super().__init__(detail=self.msg)

class UserNotFound(NotFound):
    msg = "Пользователя с таким ID не существует"

    def __init__(self):
        super().__init__(detail=self.msg)

class ProductAlreadyExists(Conflict):
    msg = "Этот товар уже в корзине"

    def __init__(self):
        super().__init__(detail=self.msg)
