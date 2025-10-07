from db.database import factory_session
from db.models import Product


def create_product(product_dt: dict):
    with factory_session() as session:
        product = Product(
            name=product_dt["product"],
            category=product_dt["category"],
            rating=product_dt["rating"],
            reviews=product_dt["reviews"],
            min_price=product_dt["min_price"],
            max_price=product_dt["max_price"],
            salesman_count=product_dt["salesman_count"],
            image_link=product_dt["image_link"]
        )
        session.add(product)
        session.commit()
