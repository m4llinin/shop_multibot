from sqlalchemy import Integer, String, Column, sql, Boolean, BigInteger
from database.db_gino import TimedBaseModel


class Payment(TimedBaseModel):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    cart = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    is_paid = Column(Boolean, default=False)

    query: sql.select
