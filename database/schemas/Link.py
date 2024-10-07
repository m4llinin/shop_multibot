from sqlalchemy import Integer, BigInteger, String, Column, sql, DateTime, ARRAY, ForeignKey
from database.db_gino import TimedBaseModel


class Link(TimedBaseModel):
    __tablename__ = 'links'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    shop_id = Column(BigInteger, nullable=False)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    all_visits = Column(BigInteger, default=0)
    unique_visits = Column(ARRAY(BigInteger), default=[])
    profit = Column(BigInteger, default=0)

    query: sql.select
