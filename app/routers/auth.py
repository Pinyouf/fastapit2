from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session


from .. import database, schemas, models, utils,oauth2


router = APIRouter(
    tags=["Authentication"]
)

#@router.post('/login', status_code=status.HTTP_200_OK)
#def login(user_credentials:schemas.UserLogin,db: Session = Depends(database.get_db)):
    #user = db.query(models.User).filter(models.User.email==user_credentials.email).first()

    #if not user:
        #raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Imvalid Credential")
    #if not utils.verify(user_credentials.password,user.password):
        #raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    #access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    #return{"token": access_token, "token_type": "bearer"}

# The above code defines a POST endpoint for user login. It takes the user's email and password as input, verifies the credentials against the database, and if valid, generates an access token using the `create_access_token` function from the `oauth2` module. The access token is then returned in the response along with the token type (bearer). If the credentials are invalid, an HTTPException with a 403 Forbidden status code is raised.

@router.post('/login', response_model=schemas.Token, status_code=status.HTTP_200_OK)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email==user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Imvalid Credential")
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    return schemas.Token(access_token=access_token, token_type="bearer")
