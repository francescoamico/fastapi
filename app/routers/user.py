from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_users(user: schemas.UserCreate, db: Session=Depends(get_db)):
    try:
        user.password = utils.hash(user.password)
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail=f"{user.email} already exists")

@router.get("/{id}", response_model=schemas.User)
def get_users(id: int, db: Session=Depends(get_db)):
    post = db.query(models.User).filter(models.User.id == id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"user {id} was not found")
    return post