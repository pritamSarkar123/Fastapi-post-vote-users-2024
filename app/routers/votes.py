from typing import List, Optional

from fastapi import APIRouter, Depends, Path, Query, Request, Response, status
from sqlalchemy.exc import IntegrityError

from ..database import Session, engine, get_db
from ..exceptions import (
    DataIntigrityError,
    PostNotFound,
    UnouthorizedToManipulatePost,
    VoteConflict,
    VoteNotFound,
)
from ..models import Post, User, Vote
from ..schemas import auth_schemas, post_schemas, vote_schemas
from ..utils import oauth2
from ..utils.rate_limit_handler import rate_limiter

router = APIRouter(
    prefix="/api/v2/vote",
    tags=["Vote"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
# @rate_limiter(max_requests=10, period=60) #TODO stopped for testing
def vote(
    request: Request,
    vote: vote_schemas.Vote,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
):
    target_post = db.query(Post).filter(Post.id == vote.post_id).first()
    if not target_post:
        raise PostNotFound(vote.post_id)

    if target_post.owner_id == current_user.id:
        raise VoteConflict(
            f"user {current_user.id} can not vote his own post {vote.post_id}"
        )

    vote_query = db.query(Vote).filter(
        Vote.post_id == vote.post_id, Vote.user_id == current_user.id
    )
    found_already_voted_post_by_user = vote_query.first()
    if vote.vote_dir == 1:
        if found_already_voted_post_by_user:
            raise VoteConflict(
                f"user {current_user.id} has already voted on the post {vote.post_id}"
            )
        else:
            new_vote = Vote(post_id=vote.post_id, user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message": "successfully added vote"}
    else:
        if not found_already_voted_post_by_user:
            raise VoteNotFound(
                f"vote of the user {current_user.id} against the post {vote.post_id} does not exists"
            )
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "successfully deleted vote"}
