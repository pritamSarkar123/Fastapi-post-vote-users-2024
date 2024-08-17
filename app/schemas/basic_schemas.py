from typing import Optional

from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True  # default nearly means optional
    # rating: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "This is the title of the post",
                "content": "This is the content of the post",
                "published": False,
                # "rating": 2,
            }
        }


class UpdatePost(BaseModel):
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool]
    rating: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "title": "This is the title of the post",
                "content": "This is the content of the post",
                "published": False,
                "rating": 2,
            }
        }
