from fastapi import Depends, HTTPException, status, APIRouter
from .. import schemas, models, utils
from sqlalchemy.orm import Session
from ..database import get_db

# Note then when we use /users fastapi uses a 307 and redirects to /users/
# It's important to understand this for testing purposes, 
# see that in all testing we directly use /users/ (pytest)
# INFO:     127.0.0.1:54730 - "POST /users HTTP/1.1" 307 Temporary Redirect
# INFO:     127.0.0.1:54730 - "POST /users/ HTTP/1.1" 200 OK

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f'User with email {user.email} already exists')
    
    # Hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id: {id} does not exist.')
        
    return user