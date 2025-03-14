from jose import JWTError,jwt
from datetime import datetime,timedelta, timezone
from . import schemas,models,database
from sqlalchemy.orm import Session
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "36f4f30d47c5758f16235fd600aa95343fe01250e6f18b8fa25e2af564c9422a"
algorithm = "HS256"
ACCESS_TOKEN_EXPIRATION_MINUTES= 30

def create_access_token(data : dict):   
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=algorithm)

    return encoded_jwt


def verify_access_token(token : str, credentials_exception):
    
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=algorithm)
        id : str = payload.get("user_id")
        
        if id is None:
            raise crendentials_exception
        
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token : str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate",  headers={"WWW-Authenticate" : "Bearer"})

    token = verify_access_token(token,credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user