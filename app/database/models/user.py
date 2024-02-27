from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.database.models.base import BaseTable


class User(BaseTable):
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    phone = Column(String, nullable=False)
