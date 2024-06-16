from database.db_gino import TimedBaseModel
from sqlalchemy import Integer, String, Column, sql, ForeignKey, BigInteger


class Order(TimedBaseModel):
    __tablename__ = "orders"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    shop_id = Column(BigInteger, nullable=False)
    user_id = Column(Integer, nullable=False)
    good_id = Column(Integer)
    good_name = Column(String)
    count = Column(Integer, default=1)
    total_price = Column(Integer, nullable=False)
    status = Column(String, default="wait pay")
    last_message_id = Column(BigInteger)

    query: sql.select
