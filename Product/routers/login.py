from fastapi import APIRouter
from ..import schema 

router = APIRouter(
    tags=["Login"],
    prefix="/login"
)

@router.post('/')
def login(request:schema.login):
    return request


