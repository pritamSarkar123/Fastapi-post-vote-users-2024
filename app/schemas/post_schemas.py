from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .user_schemas import UserResponse


class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True  # default nearly means optional

    class Config:
        schema_extra = {
            "example": {
                "title": "This is the title of the post",
                "content": "This is the content of the post",
                "published": False,
            }
        }


class CreatePost(PostBase):
    pass


class UpdatePost(PostBase):
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool]


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class PostResponseWithVote(BaseModel):
    # model name : schema name
    # it came in name "Post"
    # RMKeyView(["Post", "votes"])
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True
