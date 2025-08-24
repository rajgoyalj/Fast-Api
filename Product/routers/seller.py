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

router = APIRouter(
    tags=["Sellers"],
    prefix="/sellers"
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get('/')
def seller(db: Session = Depends(get_db)):
    seller = db.query(models.Seller).all()
    return seller


@router.get('/{id}')
def get_All_Seller(id: int, db: Session = Depends(get_db)):
    seller = db.query(models.Seller).filter(models.Seller.id == id).first()
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Seller with id {id} not found')
    return seller


@router.post('/', response_model=schema.Display_seller,status_code=status.HTTP_201_CREATED)
def create_seller(request:schema.seller, db: Session = Depends(get_db)):
    hashedpassword = pwd_context.hash(request.password)
    new_seller = models.Seller(userName=request.userName, email=request.email, password=hashedpassword, phone=request.phone)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller


@router.put('/{id}')
def update_seller(id: int, request: schema.seller, db: Session = Depends(get_db)):
    seller = db.query(models.Seller).filter(models.Seller.id == id)
    if not seller.first():
        return {'message': 'Seller not found'}
    seller.update(request.dict())
    db.commit()
    return {'message': 'Seller updated successfully'}


@router.delete('/{id}')
def delete_seller(id: int, db: Session = Depends(get_db)):
    seller = db.query(models.Seller).filter(models.Seller.id == id).delete(synchronize_session=False)
    db.commit()
    return {'message': 'Seller deleted successfully'}   