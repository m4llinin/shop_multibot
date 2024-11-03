from database.db_gino import TimedBaseModel
from sqlalchemy import Integer, String, Column, sql


class Category(TimedBaseModel):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    weight = Column(Integer, nullable=False, default=0)
    photo = Column(String)

    query: sql.select
