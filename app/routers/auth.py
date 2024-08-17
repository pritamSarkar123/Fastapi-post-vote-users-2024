from fastapi import APIRouter, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..models import User

from ..database import Session, engine, get_db
from ..exceptions import InvalidUserCredentials
from ..schemas import auth_schemas, user_schemas
from ..utils import hash_password, oauth2

router = APIRouter(
    prefix="/api/v2/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=auth_schemas.AllTokenResponse,
)
def login(
    user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == user_creds.username).first()
    if not user:
        raise InvalidUserCredentials("Invalid Credentials")
    if not hash_password.verify(user_creds.password, user.password):
        raise InvalidUserCredentials("Invalid Credentials")

    access_token = oauth2.create_access_token(
        data={
            "user_id": user.id,
        }
    )
    refresh_token = oauth2.create_refresh_token(
        data={
            "user_id": user.id,
        }
    )

    return auth_schemas.AllTokenResponse(
        **{
            "refresh_token": refresh_token,
            "access_token": access_token,
            "token_type": "bearer",
        }
    )


@router.post("/refresh", response_model=auth_schemas.AccessTokenResponse)
def refresh_token(
    refresh_token: auth_schemas.RefreshToken, db: Session = Depends(get_db)
):
    cu = oauth2.verify_token(
        refresh_token.refresh_token, InvalidUserCredentials("Invalid Credentials")
    )
    user = db.query(User).filter(User.id == cu.id).first()
    if not user:
        raise InvalidUserCredentials("Invalid Credentials")

    access_token = oauth2.create_access_token(
        data={
            "user_id": user.id,
        }
    )

    return auth_schemas.AccessTokenResponse(
        **{
            "access_token": access_token,
            "token_type": "bearer",
        }
    )
