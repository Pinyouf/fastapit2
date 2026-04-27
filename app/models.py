from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import null, text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    owner = relationship("User")
# The above code defines a SQLAlchemy model for a "Post" entity. It specifies the table name as "posts" and defines the columns for the table, including an auto-incrementing primary key "id", a non-nullable string column "title", a non-nullable string column "content", and a boolean column "published" with a default value of True. This model can be used to interact with the corresponding database table when performing CRUD operations in the application.

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String, nullable=True)
# The above code defines a SQLAlchemy model for a "User" entity. It specifies the table name as "users" and defines the columns for the table, including an auto-incrementing primary key "id", a non-nullable string column "email" that must be unique, a non-nullable string column "password", and a timestamp column "created_at" that defaults to the current time when a new user is created. This model can be used to interact with the corresponding database table when performing CRUD operations related to users in the application.

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
# The above code defines a SQLAlchemy model for a "Vote" entity. It specifies the table name as "votes" and defines two columns: "user_id" and "post_id". Both columns are foreign keys that reference the "id" columns in the "users" and "posts" tables, respectively. Additionally, both columns are set as primary keys, which means that each combination of user_id and post_id must be unique in the votes table. This model can be used to represent a many-to-many relationship between users and posts, where a user can vote on multiple posts and a post can receive votes from multiple users.

