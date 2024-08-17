from fastapi import Request, status
from fastapi.responses import JSONResponse


class DataIntigrityError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name


############################################## handlers ###########################################
def data_intigrity_error_handler(request: Request, exc: DataIntigrityError):
    return JSONResponse(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        content={"message": f"Data intigrity issue : {exc.name}"},
    )
