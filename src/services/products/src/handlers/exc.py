from src.core.exc import NotFound, Conflict

class ProductNotFound(NotFound):
    msg = "Продукт с таким ID отсутствует"

    def __init__(self):
        super().__init__(detail=self.msg)


