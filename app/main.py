from fastapi import FastAPI
from .router import auth, user, post

from .database import engine
from . import models


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

    
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(post.router)

@app.get('/')
async def root():
    return {'message' : 'Welcome to API!!!'}



    


