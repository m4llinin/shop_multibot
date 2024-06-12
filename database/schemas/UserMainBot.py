from database.db_gino import TimedBaseModel
from sqlalchemy import Integer, Float, String, Column, ARRAY, sql, BigInteger


class UserMainBot(TimedBaseModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    balance = Column(Float, default=0)
    loyalty_level = Column(Integer, default=50)
    shops = Column(ARRAY(BigInteger), default=[])
    status = Column(String, default="consumer")

    query: sql.select
