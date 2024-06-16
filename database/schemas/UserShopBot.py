from database.db_gino import TimedBaseModel
from sqlalchemy import Float, Column, sql, BigInteger, ForeignKey


class UserShopBot(TimedBaseModel):
    __tablename__ = 'shop_users'
    id = Column(BigInteger, primary_key=True)
    shop_id = Column(BigInteger, nullable=False)
    balance = Column(Float, default=0)
    referral_id = Column(BigInteger)

    query: sql.select
