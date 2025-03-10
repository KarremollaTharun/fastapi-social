from fastapi import FastAPI,HTTPException,status,Response,APIRouter,Depends
from .. import models,schemas,utils
from ..database import get_db
from sqlalchemy.orm import Session
from .. import oauth2

router = APIRouter(prefix='/posts',tags=['Posts'])

@router.get('/',response_model = list[schemas.Post])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit : int = 10,skip : int =0, search : str = ""):
    details = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return details

@router.get('/{id}',response_model = schemas.Post)
def get_posts(id : int ,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    details = db.query(models.Post).filter(models.Post.id == id).first()
    if not details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with id : {id} not found')
    
    
    return details


@router.post('/',status_code = status.HTTP_201_CREATED,response_model = schemas.Post)
def create_posts(post :schemas.PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
     
    
    new_post = models.Post(user_id = current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return  new_post

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db : Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id: {id} not found')
    
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='not authorized to do the requested action')
   
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id : int,post : schemas.PostCreate, db : Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    old_post = post_query.first()


    if not old_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'post with id : {id} not found' )  
    

    post_query.update(post.dict(),synchronize_session=False)

    db.commit()

    return post_query.first()