from database.db_gino import TimedBaseModel
from sqlalchemy import Integer, Float, String, Column, sql, ForeignKey, Boolean, BigInteger


class Shop(TimedBaseModel):
    __tablename__ = 'shops'
    id = Column(BigInteger, primary_key=True, nullable=False)
    owner_id = Column(BigInteger)
    token = Column(String, nullable=False)
    username = Column(String)
    name = Column(String)
    description = Column(String, default='')
    short_description = Column(String, default='')
    notifications = Column(Boolean, default=True)
    extra_charge = Column(Integer, default=0)
    channel = Column(String)
    is_on = Column(Boolean, default=True)

    query: sql.select
