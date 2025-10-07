from pydantic import BaseModel

class ProductValid(BaseModel):
    product: str
    category: str
    min_price: int
    max_price: int
    rating: int
    reviews: int