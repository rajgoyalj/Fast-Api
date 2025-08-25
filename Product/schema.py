from pydantic import BaseModel
from Product.models import Product
from typing import Optional

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




class login(BaseModel):
    email: str
    password: str
    class Config:
        orm_mode = True 


class Token(BaseModel):
    access_token: str
    token_type: str


# hold the username of the token holder 
class TokenData(BaseModel):
    username: Optional[str] = None