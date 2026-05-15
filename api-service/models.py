from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime
)

from database import Base

import datetime


# ================================
# TRANSACTION MODEL
# ================================
class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(String(50), primary_key=True)

    user_id = Column(String(50))

    amount = Column(Float)

    category = Column(String(50))

    timestamp = Column(
        DateTime,
        default=datetime.datetime.utcnow
    )

    status = Column(String(20))


# ================================
# USER MODEL
# ================================
class User(Base):

    __tablename__ = "users"

    id = Column(
        String(50),
        primary_key=True
    )

    username = Column(
        String(100),
        unique=True
    )

    password = Column(String(255))