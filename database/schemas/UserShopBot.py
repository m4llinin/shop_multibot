from database.db_gino import TimedBaseModel
from sqlalchemy import Float, Column, sql, BigInteger, ForeignKey, String


class UserShopBot(TimedBaseModel):
    __tablename__ = 'shop_users'
    table_id = Column(BigInteger, primary_key=True, autoincrement=True)
    id = Column(BigInteger, nullable=False)
    shop_id = Column(BigInteger, nullable=False)
    balance = Column(Float, default=0)
    referral_id = Column(BigInteger)
    link = Column(String)

    query: sql.select
