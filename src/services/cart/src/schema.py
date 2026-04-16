from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    BigInteger,
)

metadata = MetaData()

products = Table(
    "products",
    metadata,
    Column("product_id", Integer, nullable=False, primary_key=True),
    Column("user_id", Integer, nullable=False, primary_key=True),
    Column("price", BigInteger, nullable=False),
    Column("quantity", Integer, nullable=False),
)

