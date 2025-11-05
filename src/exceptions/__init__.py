from fastapi import HTTPException

class AppExecption(HTTPException):
    def __init__(
        self, 
        status_code: int, 
        detail: str,
    ):
        """ 
        Custom exception class
        """
        super().__init__(
            status_code=status_code,
            detail=detail,
            )
        