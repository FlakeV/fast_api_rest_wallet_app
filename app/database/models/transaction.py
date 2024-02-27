from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from app.database.models.base import BaseTable, Currency


class Transaction(BaseTable):
    user_id = ForeignKey("User.id", ondelete="CASCADE")
    wallet_id_from = ForeignKey("Wallet.id", ondelete="CASCADE")
    wallet_id_to = ForeignKey("Wallet.id", ondelete="CASCADE")
    amount = Column(Integer, nullable=False)
    currency = Column(Enum(Currency), nullable=False)
