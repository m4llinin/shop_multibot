from sqlalchemy import Integer, String, Column, sql
from database.db_gino import TimedBaseModel


class Request(TimedBaseModel):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    platform = Column(String, nullable=False)
    experience = Column(String, nullable=False)
    source = Column(String, nullable=False)
    admin_id = Column(Integer)
    status = Column(String, default="wait")

    query: sql.select
