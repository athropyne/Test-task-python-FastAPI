from sqlalchemy import select, CursorResult, case, exists

from src.core.interfaces import PGConnection
from src.handlers.calculate_product_quantities.exc import ThereIsNotEnoughProduct
from src.handlers.event import OrderCreatedEvent
from src.schema import reserve, products, TransactionStatus

class CalculateProductQuantitiesUOW(PGConnection):

    async def call(self, model: OrderCreatedEvent):
        products_ids = [product.product_id for product in model.products]
        stmt = (
            select(products.c.id, products.c.quantity)
            .where(products.c.id.in_(products_ids))
        )
        cursor: CursorResult = await self().execute(stmt)
        result = cursor.mappings().fetchall()
        result = [dict(product) for product in result]

        for model_product in model.products:
            for result_product in result:
                if model_product.product_id == result_product["id"]:
                    if model_product.quantity > result_product["quantity"]:
                        raise ThereIsNotEnoughProduct

        rows = [{
            "transaction_id": model.transaction_id,
            "product_id":     p.product_id,
            "quantity":       p.quantity,
        } for p in model.products]
        stmt = (
            reserve
            .insert()
            .values(rows)
        )
        await self().execute(stmt)

        stmt = (
            products
            .update()
            .where(products.c.id.in_(products_ids))
            .values(
                quantity=case(
                    *[
                        (products.c.id == product.product_id,
                         products.c.quantity - product.quantity)
                        for product
                        in model.products
                    ],
                    else_=products.c.quantity,
                ),
            )
        )
        await self().execute(stmt)

    async def commit(self, model: OrderCreatedEvent):
        stmt = (
            reserve
            .update()
            .values(status=TransactionStatus.SUCCESS)
            .where(reserve.c.transaction_id == model.transaction_id)
        )
        await self().execute(stmt)

    async def rollback(self, model: OrderCreatedEvent):
        stmt = select(exists().where(reserve.c.transaction_id == model.transaction_id))
        is_transaction_exist = await self().scalar(stmt)
        if not is_transaction_exist: return
        products_ids = [product.product_id for product in model.products]
        stmt = (
            products
            .update()
            .where(products.c.id.in_(products_ids))
            .values(
                quantity=case(
                    *[
                        (
                            products.c.id == product.product_id,
                            products.c.quantity + product.quantity
                        )
                        for product
                        in model.products
                    ],
                    else_=products.c.quantity,
                ),
            )
        )
        await self().execute(stmt)

        stmt = (
            reserve
            .update()
            .values(status=TransactionStatus.FAILED)
            .where(reserve.c.transaction_id == model.transaction_id)
        )
        await self().execute(stmt)