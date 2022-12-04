from sqlalchemy import Column, Unicode, BigInteger, Boolean, String, String

from core.db import Base
from core.db.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    password = Column(Unicode(255), nullable=False)
    email = Column(Unicode(255), nullable=False, unique=True)
    name = Column(Unicode(255), nullable=False)
    organization = Column(String(100), nullable=True)
    is_admin = Column(Boolean, default=False)
