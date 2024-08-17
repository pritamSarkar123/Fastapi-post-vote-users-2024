from fastapi import Request, status
from fastapi.responses import JSONResponse


class UserNotFound(Exception):
    def __init__(self, name: str) -> None:
        self.name = name


class InvalidUserCredentials(Exception):
    def __init__(self, name: str) -> None:
        self.name = name


############################################## handlers ###########################################
def user_not_found_handler(request: Request, exc: UserNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"user with id : {exc.name} cannot be found."},
    )


def invalid_creds_handler(request: Request, exc: InvalidUserCredentials):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"message": f"{exc.name}"},
        headers={"WWW-Authenticate": "Bearer"},
    )
