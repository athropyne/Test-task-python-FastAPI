import enum

from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    BigInteger, ForeignKey, DateTime, func, Enum, String, Boolean,
)

metadata = MetaData()

class OrderStatus(enum.Enum):
    PREPARING = "собирается"
    READY = "готов"
    REJECTED = "отклонен"

    @classmethod
    def values(cls):
        return lambda x: [x.value for x in x]

OS = OrderStatus
orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False),
    Column("status", Enum(OS, values_callable=OS.values()), nullable=False, default=OS.PREPARING),
    Column("profile_service_ok", Boolean, nullable=True, default=None),
    Column("product_service_ok", Boolean, nullable=True, default=None),
    Column("rejected_reason", String, nullable=True, default=None),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
)
products = Table(
    "products",
    metadata,
    Column("order_id", ForeignKey(orders.c.id, ondelete="CASCADE"), nullable=False),
    Column("product_id", Integer, nullable=False),
    Column("price", BigInteger, nullable=False),
    Column("quantity", Integer, nullable=False),
)
