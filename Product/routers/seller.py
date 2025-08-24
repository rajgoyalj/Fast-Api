from fastapi import FastAPI,APIRouter
from fastapi import FastAPI,Response,HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from  ..import models
from ..import schema
from passlib.context import CryptContext
from ..database import get_db
from fastapi import status
from typing import List

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get('/sellers',tags=["Sellers"])
def seller(db: Session = Depends(get_db)):
    seller = db.query(models.Seller).all()
    return seller

@router.post('/sellers', response_model=schema.Display_seller,tags=["Sellers"])
def create_seller(request:schema.seller, db: Session = Depends(get_db)):
    hashedpassword = pwd_context.hash(request.password)
    new_seller = models.Seller(userName=request.userName, email=request.email, password=hashedpassword, phone=request.phone)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller
