from .. import models, schemas, oauth2
from fastapi import   Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import  get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# if you want to only return the posts created by the logged in user, you can use the following code:
#@router.get("/",response_model=list[schemas.Post])
#def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):   
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() # type: ignore
    #return posts

# if you want to return all the posts created by all the users, you can use the following code:
#@router.get("/",response_model=list[schemas.Post])
#def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):   
    #posts = db.query(models.Post).all() # type: ignore        
    #return posts

# if you want to return a limited number of posts, you can use the following code:
# @router.get("/",response_model=list[schemas.Post])
# def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 4):   
#     posts = db.query(models.Post).limit(limit).all() # type: ignore    
#     return posts

# implement search functionality to search for posts by title or content
#@router.get("/",response_model=list[schemas.Post])
@router.get("/",response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 4, search: Optional[str] = ""):   
    #posts = db.query(models.Post).filter(models.Post.title.contains(search) | models.Post.content.contains(search)).limit(limit).all() # type: ignore    
    #print(posts)
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search) | models.Post.content.contains(search)).limit(limit).all() # type: ignore
    
    return posts
    

# Create a new post
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    print(f"User ID from token: {current_user.id}") # type: ignore
    
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())     # type: ignore
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post
# The above code defines a POST endpoint that allows clients to create a new post. It takes parameters for the post's title, content, and published status. The endpoint executes an SQL INSERT statement to add the new post to the database and returns the newly created post in the response. The status code for a successful creation is set to 201 Created.
    
# Get a specific post by ID
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    #cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    #post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first() # type: ignore
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found.")
    #if post.owner_id != current_user.id: # type: ignore
        #raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            #detail=f"Not authorized to perform requested action.")
    return post
# The above code defines a GET endpoint that retrieves a specific post by its ID.
# The use of HTTPException provides a more standardized way to handle errors and return appropriate status codes in the response.

# Delete a post by ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found.")
    if post.owner_id != current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action.")
    #db.delete(post)
    post_query.delete(synchronize_session=False) # type: ignore
    db.commit()
    print(f"Post with id {id} deleted successfully.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
# The above code defines a DELETE endpoint that allows clients to delete a specific post by its ID. It first checks if the post exists in the database by executing a SELECT statement. If the post is not found, it raises an HTTPException with a 404 Not Found status code. If the post is found, it executes a DELETE statement to remove the post from the database and commits the transaction. Finally, it returns a response with a 204 No Content status code to indicate that the deletion was successful.

# Update a post by ID
@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found.")

    if post.owner_id != current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action.")
    post_query.update(updated_post.model_dump(), synchronize_session=False) # type: ignore
    
    db.commit()
    
    print(f"Post with id {id} updated successfully.")
    return post_query.first()
# The above code defines a PUT endpoint that allows clients to update an existing post by its ID. It first checks if the post exists in the database by executing a SELECT statement. If the post is not found, it raises an HTTPException with a 404 Not Found status code. If the post is found, it executes an UPDATE statement to modify the post's title, content, and published status based on the provided data. The updated post is returned in the response after committing the transaction to the database.
