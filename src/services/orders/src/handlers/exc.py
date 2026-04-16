from src.core.exc import ClientError

class EmptyProductList(ClientError):
    msg = "Корзина пуста"

    def __init__(self):
        super().__init__(detail=self.msg)
