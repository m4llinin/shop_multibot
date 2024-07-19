from sqlalchemy import Integer, String, Column, sql, BigInteger
from database.db_gino import TimedBaseModel


class Request(TimedBaseModel):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    platform = Column(String, nullable=False)
    experience = Column(String, nullable=False)
    source = Column(String, nullable=False)
    admin_id = Column(Integer)
    status = Column(String, default="wait")

    query: sql.select
