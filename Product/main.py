from fastapi import FastAPI
from  .import models
from .database import  engine
from .routers import product
from .routers import seller, login


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
app.include_router(seller.router)
app.include_router(login.router)


models.Base.metadata.create_all(engine)








