import enum
from sqlalchemy import Column, Integer, inspect
from sqlalchemy.orm import declared_attr, declarative_base

Base = declarative_base()


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


class BaseTable(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()


class Currency(enum.Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
