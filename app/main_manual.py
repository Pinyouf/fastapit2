

from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    rating: Optional[int] = None

    
my_posts = [{"title": "Title of post 1", "content": "This is the content of post 1","id": 1, "published": True, "rating": 5},
            {"title": "Title of post 2", "content": "This is the content of post 2","id": 2, "published": False, "rating": None}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None
# The above code defines a function called find_post that takes an id as an argument and searches through the my_posts list to find a post with a matching id. If a post is found, it returns the post; otherwise, it returns None. This function is useful for retrieving specific posts based on their unique identifiers.

def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
    return None
# The above code defines a function called find_index_post that takes an id as an argument and searches through the my_posts list to find the index of a post with a matching id. It uses the enumerate function to iterate through the list while keeping track of the index. If a post with the specified id is found, it returns the index; otherwise, it returns None. This function can be useful for operations that require modifying or deleting a post based on its index in the list.


@app.get("/")
def root():
    return {"Message": "Welcome to FastAPI!"}

@app.get("/posts")
def get_posts():
    return {"Posts": "List of posts will be here."}

#@app.post("/createposts")
#def create_posts(payload: dict=Body(...)):
    #print(payload)
    ##return {"Message": "Post created successfully!"}
    #return {"new_post": f"title: {payload['title']}, content: {payload['content']}"}

#the above code is not recommended because it does not validate the input data and can lead to errors if the expected keys are missing or have incorrect types. Using Pydantic models, as shown in the next example, provides better validation and error handling.

@app.post("/createposts")
def create_posts(new_post: Post):    
    print(new_post)
    print(new_post.title)
    #print(new_post.dict())
    print(new_post.model_dump())

    return {"data":"New post created successfully!"}
# The above code is better because it uses a Pydantic model (Post) to validate the input data. This ensures that the required fields are present and have the correct types, reducing the likelihood of errors and improving the overall robustness of the API.

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data":"New post created successfully!"}
# the above code adds the new post to the my_posts list and returns a success message. The use of the Post model ensures that the input data is validated before being added to the list.
# The status_code=status.HTTP_201_CREATED parameter in the @app.post decorator indicates that the endpoint will return a 201 Created status code when a new post is successfully created. This is a standard HTTP response code that indicates that a new resource has been created as a result of the request.

@app.get("/createdposts")
def created_posts():
    return {"Posts": my_posts}
# The above code defines a GET endpoint that returns the list of created posts stored in the my_posts variable. This allows clients to retrieve all the posts that have been created through the API.


@app.get("/posts/latest")
def get_latest_post():
    post  = my_posts[len(my_posts)-1]
    return {"latest_post": post}
# The above code defines a GET endpoint that retrieves the latest post from the my_posts list. It accesses the last element of the list using len(my_posts)-1 and returns it in the response. This allows clients to easily get the most recently created post.

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"Error": f"Post with id {id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found.")
    return {"post_detail": post}
# The above code defines a GET endpoint that retrieves a specific post by its ID. It uses the find_post function to search for the post in the my_posts list. If the post is not found, it returns an error message. Otherwise, it returns the details of the found post. This allows clients to access individual posts by their unique identifiers.
# The use of HTTPException provides a more standardized way to handle errors and return appropriate status codes in the response.

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #post = find_post(id)
    #if not post:
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found.")
    #my_posts.remove(post)
    #return Response(status_code=status.HTTP_204_NO_CONTENT)
# The above code defines a DELETE endpoint that allows clients to delete a specific post by its ID. It uses the find_post function to search for the post in the my_posts list. If the post is not found, it raises an HTTPException with a 404 Not Found status code. If the post is found, it removes the post from the my_posts list and returns a response with a 204 No Content status code, indicating that the deletion was successful and there is no content to return in the response body.

    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found.")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
# The above code defines a DELETE endpoint that allows clients to delete a specific post by its ID. It uses the find_index_post function to search for the index of the post in the my_posts list. If the index is None, it raises an HTTPException with a 404 Not Found status code. If the index is found, it removes the post from the my_posts list using the pop method and returns a response with a 204 No Content status code, indicating that the deletion was successful and there is no content to return in the response body.

@app.put("/posts/{id}")
def update_post(id: int, updated_post: UpdatePost):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found.")
    
    post_dict = updated_post.model_dump(exclude_unset=True)
    for key, value in post_dict.items():
        my_posts[index][key] = value
    
    return {"data": "Post updated successfully!"}
# The above code defines a PUT endpoint that allows clients to update a specific post by its ID. It uses the find_index_post function to search for the index of the post in the my_posts list. If the index is None, it raises an HTTPException with a 404 Not Found status code. If the index is found, it converts the updated_post Pydantic model to a dictionary while excluding unset fields using model_dump(exclude_unset=True). It then iterates through the key-value pairs in the dictionary and updates the corresponding fields in the my_posts list at the specified index. Finally, it returns a success message indicating that the post was updated successfully.

