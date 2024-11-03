from database.db_gino import TimedBaseModel
from sqlalchemy import Integer, String, Column, sql, ForeignKey


class Good(TimedBaseModel):
    __tablename__ = 'goods'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer)
    subcategory_id = Column(Integer, default=0)
    name = Column(String, nullable=False)
    product = Column(String)
    description = Column(String)
    count = Column(Integer, default=0)
    price = Column(Integer)
    weight = Column(Integer, default=0)

    query: sql.select
