
from .. import schemas, models, utils
from fastapi import FastAPI, Response,status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db 
# -------------------------Users-----------------------------------------------------
router = APIRouter(
    prefix="/users",
    tags=['users']
)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user : schemas.UserCreate, db: Session = Depends(get_db)):
    
    #hash paswrod--user.password
    hased_password = utils.hash(user.password)
    user.password = hased_password
    user_name= db.query(models.User).filter(models.User.email == user.email).first()
    if user_name:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user name with {user.email} already exits")
    
    new_user = models.User(**user.model_dump())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#----get user based on id---
@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with id {id} not found")
    return user