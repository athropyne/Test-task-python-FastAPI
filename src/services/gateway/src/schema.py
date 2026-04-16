from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    DateTime,
    func,
)

metadata = MetaData()

accounts = Table(
    "accounts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(150), nullable=False, unique=True),
    Column("password", String(128), nullable=False),
)

services = Table(
    "services",
    metadata,
    Column("address", String, primary_key=True),
    Column("title", String, nullable=False),
    Column("created_at", DateTime, server_default=func.now()),
)