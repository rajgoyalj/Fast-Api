from pydantic import BaseModel
from Product.models import Product

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: bool

class seller(BaseModel):
    id: int
    userName: str
    email: str
    password : str
    phone : int

class Display_seller(seller):
    id: int
    userName: str
    email: str
    phone: int
    class Config:
        orm_mode = True


class ProductCreate(Product):
    name: str
    description: str
    seller:Display_seller
    class Config:
        orm_mode = True




