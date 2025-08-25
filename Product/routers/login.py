from ..schema import TokenData
from fastapi import APIRouter,Depends,status,HTTPException
from ..import schema,models
from sqlalchemy.orm import Session
from ..database import get_db
from passlib.context import CryptContext 
from datetime import datetime,timedelta
from jose import JWTError,jwt
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY="400dc3f986a732b39d5bee131ae7882616a1d93c869ee2148c2972de8c7d8da0"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

router = APIRouter(
    tags=["Login"],
    prefix="/login"
)
oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")   

def generate_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token



   

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    Seller = db.query(models.Seller).filter(models.Seller.email == request.username).first()
    if not Seller:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")
    if not pwd_context.verify(request.password, Seller.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    access_token = generate_token({"sub": Seller.email})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_User(token: str = Depends(oauth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schema.TokenData(username=username)
        return token_data
    except JWTError:
        raise credentials_exception