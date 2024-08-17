from fastapi import Request, status
from fastapi.responses import JSONResponse


class VoteNotFound(Exception):
    def __init__(self, name: str) -> None:
        self.name = name


class VoteConflict(Exception):
    def __init__(self, name: str) -> None:
        self.name = name


############################################## handlers ###########################################
def vote_not_found_handler(request: Request, exc: VoteNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.name},
    )


def vote_conflict_handler(request: Request, exc: VoteConflict):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": exc.name},
    )
