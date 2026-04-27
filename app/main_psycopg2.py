

from copy import error

from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time



app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# connecting to the database
while True:
    try:    
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", 
                            password="postgres", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successful!")
        break
    
    except Exception as error:
        print(f"Error connecting to database: {error}")
        time.sleep(2)

# The above code attempts to establish a connection to a PostgreSQL database using the psycopg2 library. It specifies the host, database name, user, password, and cursor factory for the connection. If the connection is successful, it prints a success message. If there is an error during the connection process, it catches the exception and prints an error message. Finally, it ensures that the database connection and cursor are closed properly in the finally block.
# This hardcoded connection is not recommended for production applications. Instead, consider using environment variables or a configuration file to store sensitive information like database credentials.



@app.get("/")
def root():
    return {"Message": "Welcome to FastAPI!"}

@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    #print(posts)
    return {"Posts": posts}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
                    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}
# The above code defines a POST endpoint that allows clients to create a new post. It takes parameters for the post's title, content, and published status. The endpoint executes an SQL INSERT statement to add the new post to the database and returns the newly created post in the response. The status code for a successful creation is set to 201 Created.
    

@app.get("/posts/{id}")
def get_post(id: int, response: Response):    
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"Error": f"Post with id {id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found.")
    return {"post_detail": post}
# The above code defines a GET endpoint that retrieves a specific post by its ID.
# The use of HTTPException provides a more standardized way to handle errors and return appropriate status codes in the response.

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found.")
    cursor.execute("DELETE FROM posts WHERE id = %s returning * ", (str(id),))
    conn.commit()
    print(f"Post with id {id} deleted successfully.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
# The above code defines a DELETE endpoint that allows clients to delete a specific post by its ID. It first checks if the post exists in the database by executing a SELECT statement. If the post is not found, it raises an HTTPException with a 404 Not Found status code. If the post is found, it executes a DELETE statement to remove the post from the database and commits the transaction. Finally, it returns a response with a 204 No Content status code to indicate that the deletion was successful.

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    existing_post = cursor.fetchone()
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} not found.")

    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
                    (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    print(f"Post with id {id} updated successfully.")
    return {"data": updated_post}
# The above code defines a PUT endpoint that allows clients to update an existing post by its ID. It first checks if the post exists in the database by executing a SELECT statement. If the post is not found, it raises an HTTPException with a 404 Not Found status code. If the post is found, it executes an UPDATE statement to modify the post's title, content, and published status based on the provided data. The updated post is returned in the response after committing the transaction to the database.


