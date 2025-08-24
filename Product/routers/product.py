from fastapi import APIRouter
from fastapi import FastAPI,Response,HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from  ..import models
from ..import schema
from ..database import get_db
from fastapi import status
from typing import List

router = APIRouter(
     tags=["Products"],
     prefix="/products"
)



@router.get('/')
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

# getting product by id
@router.get('/{id}', response_model=schema.ProductCreate)
def product(id: int,response: Response, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    # here we raise exception for http where not found the product
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Product with id {id} not found')     
    return product

# update the data in db 

@router.put('/{id}')
def update(id,request: schema.Product, db: Session = Depends(get_db)):
        product = db.query(models.Product).filter(models.Product.id == id)
        if not product.first():
            return {'message': 'Product not found'}
        product.update(request.dict())
        db.commit()
        return {'message': 'Product updated successfully'}

#delete the product by id 
@router.delete('/{id}')
def delete(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)    
    db.commit()
    return {'message': 'Product deleted successfully'}

#post the data to db
@router.post('/',status_code=status.HTTP_201_CREATED)
def create_product(request: schema.ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(name=request.name, description=request.description, price=request.price, quantity=request.quantity,seller_id=1)
    db.add(new_product)
    db.commit() 
    db.refresh(new_product)
    return request
