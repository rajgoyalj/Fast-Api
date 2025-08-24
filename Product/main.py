from fastapi import FastAPI,Response,HTTPException
from sqlalchemy.sql.functions import mode
from fastapi.params import Depends
from sqlalchemy.orm import Session
from  .import models
from .import schema
from .database import  engine, SessionLocal
from fastapi import status
from passlib.context import CryptContext
from .database import get_db
from .routers import product


app = FastAPI(
    title="Product API",
    description="API for managing products and sellers",
    version="1.0.0",
    terms_of_service="http://www.google.com",
    contact={
        "developer": "Raj Goyal",
        "website": "http://www.google.com",
        "email": "rajgoyalj176@gmail.com"
    },
    docs_url="/documentation",
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }

)
app.include_router(product.router)


models.Base.metadata.create_all(engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get('/sellers',tags=["Sellers"])
def seller(db: Session = Depends(get_db)):
    seller = db.query(models.Seller).all()
    return seller

@app.post('/sellers', response_model=schema.Display_seller,tags=["Sellers"])
def create_seller(request:schema.seller, db: Session = Depends(get_db)):
    hashedpassword = pwd_context.hash(request.password)
    new_seller = models.Seller(userName=request.userName, email=request.email, password=hashedpassword, phone=request.phone)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller

