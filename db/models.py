from sqlalchemy import Column, Integer, String, Float
from db.database import Base  # базовый класс SQLAlchemy

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)       # Название товара
    category = Column(String, nullable=False)   # Категория товара
    min_price = Column(Integer, nullable=True)  # Минимальная цена
    max_price = Column(Integer, nullable=True)  # Максимальная цена
    rating = Column(Float, nullable=True)       # Рейтинг
    reviews = Column(Integer, nullable=True)    # Кол-во отзывов