from enum import Enum

from pydantic import BaseModel
from pydantic.types import conint


class VoteDirection(int, Enum):
    UP = 1
    DOWN = 0


class Vote(BaseModel):
    post_id: int
    # vote_dir: conint(le1) do not use con int as it takes negatives also
    # vote_dir: conint(ge=0,le=1) will work
    vote_dir: VoteDirection

    class Config:
        schema_extra = {
            "example": {
                "post_id": "2",
                "vote_dir": 1,
            }
        }
