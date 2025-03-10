from fastapi import FastAPI,HTTPException,status,Response,APIRouter,Depends
from .. import models,schemas,utils
from ..database import get_db
from sqlalchemy.orm import Session
from .. import oauth2

router = APIRouter(
    prefix = '/users'
)

@router.post('/',status_code = status.HTTP_201_CREATED,response_model = schemas.User)
def create_user(user :schemas.User,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
     
    
    new_user = models.User(**user.dict()) 
    
    email = db.query(models.User).filter(models.User.email == new_user.email).first()   
    
    if email:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail='email already exist in db')
    hashed_password = utils.hash(new_user.password)
    new_user.password = hashed_password
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return  new_user
    
    
@router.get('/',response_model = list[schemas.User] )
def get_users(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    details = db.query(models.User).all()
    return details


@router.get('/{id}',response_model = schemas.User)
def get_users(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    details = db.query(models.User).filter(models.User.id == id).first()
    
    if not details:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f'User details with id = {id} not found')

    return  details



