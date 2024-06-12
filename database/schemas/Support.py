from database.db_gino import TimedBaseModel
from sqlalchemy import Integer, String, Column, sql, ForeignKey, BigInteger


class Support(TimedBaseModel):
    __tablename__ = 'supports'
    id = Column(Integer, primary_key=True, autoincrement=True)
    shop_id = Column(BigInteger, ForeignKey('shops.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    theme = Column(String, nullable=False)
    text = Column(String, nullable=False)
    solution = Column(String)
    admin = Column(Integer)
    status = Column(String, default="wait")

    query: sql.select
