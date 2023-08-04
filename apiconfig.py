from typing import List
from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float

class ProductList(BaseModel):
    prods: List[Product]

class User(BaseModel):
    id: int
    name: str
    phone: str | None = None
    email: str


class Cart(BaseModel):
    prods: List[Product]
    userId: int