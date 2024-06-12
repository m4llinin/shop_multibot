from database.db_gino import TimedBaseModel
from sqlalchemy import Integer, Float, String, Column, sql, ForeignKey, Boolean, BigInteger


class Shop(TimedBaseModel):
    __tablename__ = 'shops'
    id = Column(BigInteger, primary_key=True, nullable=False)
    owner_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    token = Column(String, nullable=False)
    username = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, default='')
    short_description = Column(String, default='')
    notifications = Column(Boolean, default=True)
    promo_mailing = Column(Boolean, default=True)
    extra_charge = Column(Integer, default=0)
    channel = Column(String)
    profit = Column(Float, default=0)
    sales = Column(Integer, default=0)
    users = Column(Integer, default=0)

    query: sql.select
