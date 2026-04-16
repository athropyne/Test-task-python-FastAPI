import enum

from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    BigInteger, String, ForeignKey, Enum, UUID,
)

metadata = MetaData()

products = Table(
    "products",
    metadata,
    Column("id", Integer, nullable=False, primary_key=True, autoincrement=True),
    Column("title", String(150), nullable=False),
    Column("description", String(1500), nullable=False),
    Column("cost_price", BigInteger, nullable=False),
    Column("user_price", BigInteger, nullable=False),
    Column("quantity", Integer, nullable=False),
)

class TransactionStatus(enum.Enum):
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"

    @classmethod
    def values(cls):
        return lambda x: [x.value for x in x]

TS = TransactionStatus
reserve = Table(
    "reserve",
    metadata,
    Column("transaction_id", UUID, primary_key=True),
    Column("product_id", ForeignKey(products.c.id, ondelete="CASCADE"), nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("status", Enum(TS, callable_values=TS.values()), nullable=False, default=TS.PROCESSING),
)

