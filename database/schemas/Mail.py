from sqlalchemy import Integer, BigInteger, String, Column, sql, DateTime, ARRAY
from database.db_gino import TimedBaseModel


class Mail(TimedBaseModel):
    __tablename__ = 'mails'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    shop_id = Column(ARRAY(BigInteger))
    text = Column(String)
    photo = Column(String)
    keyboard = Column(String)
    wait_date = Column(DateTime)
    loop = Column(String)
    real_date = Column(DateTime)
    all_send = Column(Integer, default=0)
    successful_send = Column(Integer, default=0)
    failed_send = Column(Integer, default=0)
    status = Column(String, default="wait")

    query: sql.select
