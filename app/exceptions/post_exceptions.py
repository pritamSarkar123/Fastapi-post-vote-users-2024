from fastapi import Request, status
from fastapi.responses import JSONResponse


class PostNotFound(Exception):
    def __init__(self, name: str) -> None:
        self.name = name


class UnouthorizedToManipulatePost(Exception):
    def __init__(self, name: str) -> None:
        self.name = name


############################################## handlers ###########################################
def post_not_found_handler(request: Request, exc: PostNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"post with id : {exc.name} cannot be found."},
    )


def unouthorize_to_manipulate_post_handler(
    request: Request, exc: UnouthorizedToManipulatePost
):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "message": f"user : {exc.name} not authorized to perform this requested action."
        },
    )
