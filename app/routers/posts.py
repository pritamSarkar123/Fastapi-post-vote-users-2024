from typing import List, Optional

from fastapi import APIRouter, Depends, Path, Query, Request, Response, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from ..database import Session, engine, get_db
from ..exceptions import DataIntigrityError, PostNotFound, UnouthorizedToManipulatePost
from ..models import Post, User, Vote
from ..schemas import auth_schemas, post_schemas
from ..utils import oauth2
from ..utils.rate_limit_handler import rate_limiter

router = APIRouter(
    prefix="/api/v2/post",
    tags=["Post"],
)


# models.Base.metadata.create_all(bind=engine)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[post_schemas.PostResponseWithVote],
)
# @rate_limiter(max_requests=10, period=60) #TODO stopped for testing
def get_posts(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=0),
    search: Optional[str] = Query(default=""),
):
    # db.query(Post) and other filters, makes the query
    # .all(), .first() executes the query
    # posts = (
    #     db.query(Post)
    #     .filter(Post.title.contains(search))
    # .offset(offset)
    # .limit(limit)
    # .all()
    # )

    # by default join in sql alchemy is ***** left inner *****
    posts = (
        db.query(Post, func.count(Vote.post_id).label("votes"))
        .join(Vote, Post.id == Vote.post_id, isouter=True)
        .group_by(Post.id)
        .filter(Post.title.contains(search))
        .offset(offset)
        .limit(limit)
        .all()
    )
    return posts


@router.get(
    "/owned",
    status_code=status.HTTP_200_OK,
    response_model=List[post_schemas.PostResponseWithVote],
)
# @rate_limiter(max_requests=10, period=60) #TODO stopped for testing
def get_owned_posts(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=0),
    search: Optional[str] = Query(default=""),
):
    # db.query(Post) and other filters, makes the query
    # .all(), .first() executes the query
    posts = (
        db.query(Post, func.count(Vote.post_id).label("votes"))
        .join(Vote, Post.id == Vote.post_id, isouter=True)
        .group_by(Post.id)
        .filter(Post.owner_id == current_user.id)
        .filter(Post.title.contains(search))
        .offset(offset)
        .limit(limit)
        .all()
    )
    return posts


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=post_schemas.PostResponseWithVote,
)
# @rate_limiter(max_requests=10, period=60) #TODO stopped for testing
def get_single_post(
    request: Request,
    id: int = Path(),
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
):
    post = (
        db.query(Post, func.count(Vote.post_id).label("votes"))
        .join(Vote, Post.id == Vote.post_id, isouter=True)
        .group_by(Post.id)
        .filter(Post.id == id)
        .first()
    )
    # print(type(post)) <class 'sqlalchemy.engine.row.Row'>
    # print(post.keys()) RMKeyView(['Post', 'votes']) # based on this we need to make the return schema
    if not post:
        raise PostNotFound(id)
    return post


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=post_schemas.PostResponse
)
# @rate_limiter(max_requests=10, period=60)#TODO stopped for testing
def create_post(
    request: Request,
    post: post_schemas.CreatePost,
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
):
    try:
        new_post = Post(owner_id=current_user.id, **post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)  # returning
        return new_post
    except IntegrityError as e:
        raise DataIntigrityError(e.args[0])


@router.put("/{id}", response_model=post_schemas.PostResponse)
# @rate_limiter(max_requests=10, period=60) #TODO stopped for testing
def update_post(
    request: Request,
    post: post_schemas.UpdatePost,
    id: int = Path(),
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
):
    try:
        updating_post = db.query(Post).filter(Post.id == id)
        updated_post = updating_post.first()
        if not updated_post:
            raise PostNotFound(id)

        if current_user.id != updated_post.owner_id:
            raise UnouthorizedToManipulatePost(current_user.id)
        updating_post.update(post.dict(), synchronize_session=False)
        db.commit()
        return updating_post.first()  # equivalent to returning
    except IntegrityError as e:
        raise DataIntigrityError(e.args[0])


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# @rate_limiter(max_requests=10, period=60) #TODO stopped for testing
def delete_post(
    request: Request,
    id: int = Path(),
    db: Session = Depends(get_db),
    current_user: User = Depends(oauth2.get_current_user),
):
    deleting_post = db.query(Post).filter(Post.id == id)
    deleted_post = deleting_post.first()
    if not deleted_post:
        raise PostNotFound(id)

    if current_user.id != deleted_post.owner_id:
        raise UnouthorizedToManipulatePost(current_user.id)
    deleting_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
