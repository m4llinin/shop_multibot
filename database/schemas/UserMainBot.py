from database.db_gino import TimedBaseModel
from sqlalchemy import Integer, Float, String, Column, ARRAY, sql, BigInteger, DateTime, Boolean


class UserMainBot(TimedBaseModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    recover_code = Column(String)
    referral_id = Column(BigInteger)
    username = Column(String)
    balance = Column(Float, default=0)
    loyalty_level = Column(Integer, default=45)
    shops = Column(ARRAY(BigInteger), default=[])
    status = Column(String, default="partner")
    last_offer = Column(DateTime)
    is_ban = Column(Boolean, default=False)

    query: sql.select
