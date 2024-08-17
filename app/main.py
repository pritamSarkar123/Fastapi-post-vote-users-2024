from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Body

from .config import settings
from .database import engine
from .exceptions import (
    DataIntigrityError,
    InvalidUserCredentials,
    PostNotFound,
    UnouthorizedToManipulatePost,
    UserNotFound,
    VoteConflict,
    VoteNotFound,
    data_intigrity_error_handler,
    invalid_creds_handler,
    post_not_found_handler,
    unouthorize_to_manipulate_post_handler,
    user_not_found_handler,
    vote_conflict_handler,
    vote_not_found_handler,
)
from .exceptions.post_exceptions import PostNotFound, post_not_found_handler
from .models import Base
from .routers import auth, posts, users, votes

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


######################################## exception handlers ########################################
@app.exception_handler(PostNotFound)
async def action_post_not_found(request: Request, exc: PostNotFound):
    return post_not_found_handler(request, exc)


@app.exception_handler(DataIntigrityError)
async def action_data_intigrity_error(request: Request, exc: DataIntigrityError):
    return data_intigrity_error_handler(request, exc)


@app.exception_handler(UserNotFound)
async def action_user_not_found(request: Request, exc: UserNotFound):
    return user_not_found_handler(request, exc)


@app.exception_handler(InvalidUserCredentials)
async def invalid_creds_handle(request: Request, exc: InvalidUserCredentials):
    return invalid_creds_handler(request, exc)


@app.exception_handler(UnouthorizedToManipulatePost)
async def unauthorize_post_handle(request: Request, exc: UnouthorizedToManipulatePost):
    return unouthorize_to_manipulate_post_handler(request, exc)


@app.exception_handler(VoteNotFound)
async def vote_not_found_handle(request: Request, exc: VoteNotFound):
    return vote_not_found_handler(request, exc)


@app.exception_handler(VoteConflict)
async def vote_conflict_handle(request: Request, exc: VoteConflict):
    return vote_conflict_handler(request, exc)


######################################## exception handlers ########################################

# TODO
# Base.metadata.create_all(bind=engine)  # base of model
# above line is required one time, then alembic can take control
# or we can ommit the line then alembic can take full control from begining

# if the above line retains then also there is no issue
# as initial revision will be blank as initial table creation will already be done


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
def root():
    return {"message": "Hello world"}
