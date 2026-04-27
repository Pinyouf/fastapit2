
from datetime import datetime

from pydantic import BaseModel, EmailStr, conint
from typing import Optional, Annotated

class UserBase(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):   
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        #orm_mode = True # this code brings columns of relationship
        from_attributes = True

   
# The above code defines three Pydantic models: UserBase, UserCreate, and UserOut. The UserBase model represents the basic structure of a user with fields for email and password. The UserCreate model inherits from UserBase and can be used specifically for creating new users, with the email field validated as an EmailStr. The UserOut model represents the structure of a user when it is returned in responses, including fields for id, email, and created_at timestamp. The from_attributes configuration allows these models to work seamlessly with SQLAlchemy models when serializing data for API responses.

class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class Token(BaseModel):
    access_token: str
    token_type: str
# The above code defines two Pydantic models: UserLogin and Token. The UserLogin model represents the structure of the data required for user login, with fields for email and password. The email field is validated as an EmailStr to ensure it is a valid email address. The Token model represents the structure of the authentication token that will be returned upon successful login, with fields for the token itself and the token type (e.g., "bearer"). These models can be used for data validation and serialization when handling authentication requests and responses in the FastAPI application.
class TokenData(BaseModel):
    id: Optional[str] = None
# The above code defines a Pydantic model called TokenData. This model has a single optional field called id, which is of type string. The default value for this field is set to None. This model can be used to represent the data contained within an authentication token, such as the user ID, when decoding and validating the token in the FastAPI application.



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass
# The above code defines three Pydantic models: Post, PostBase, and PostCreate. The Post model represents the structure of a post with fields for title, content, and published status. The PostBase model is a base class that can be used for other models that share the same fields. The PostCreate model inherits from PostBase and can be used specifically for creating new posts. These models can be used for data validation and serialization when handling requests and responses in the FastAPI application.

class Post(PostBase):
    id: int
    created_at: datetime
    #owner_id: int   
    owner: UserOut
    
    class Config:
        from_attributes = True

class Vote(BaseModel):
    post_id:int
    dir: Annotated[int, conint(le=1)]

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True