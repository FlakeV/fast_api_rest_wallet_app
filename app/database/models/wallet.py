from sqlalchemy import Column, Integer, ForeignKey, Enum

from app.database.models.base import BaseTable, Currency


class Wallet(BaseTable):
    user_id = Column(Integer, ForeignKey("user.id"))
    balance = Column(Integer, nullable=False)
    Currency = Column(Enum(Currency), nullable=False)
