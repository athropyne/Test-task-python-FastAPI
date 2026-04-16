import enum

from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    BigInteger, String, Enum, ForeignKey, UUID,
)

metadata = MetaData()

profiles = Table(
    "profiles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False, unique=True),
    Column("balance", BigInteger, nullable=False, default=0),
)

class TransactionStatus(enum.Enum):
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"

    @classmethod
    def values(cls):
        return lambda x: [x.value for x in x]

TS = TransactionStatus
debts = Table(
    "debts",
    metadata,
    Column("transaction_id", UUID, primary_key=True),
    Column("profile_id", ForeignKey(profiles.c.id, ondelete="CASCADE"), nullable=False),
    Column("amount", BigInteger, nullable=False),
    Column("status", Enum(TS, callable_values=TS.values()), nullable=False, default=TS.PROCESSING),
)
