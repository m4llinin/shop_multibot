from database.db_gino import TimedBaseModel
from sqlalchemy import Integer, String, Column, sql, ForeignKey


class Subcategory(TimedBaseModel):
    __tablename__ = 'subcategories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer)
    name = Column(String, nullable=False)
    description = Column(String)

    query: sql.select
