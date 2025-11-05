from . import AppExecption


class ErrorToken(AppExecption):
    def __init__(self, detail):
        super().__init__(400, detail)

class Unauthorized(AppExecption):
    def __init__(self, detail: str = "Unauthorized 😳"):
        super().__init__(401, detail)
    

class NotAllowed(AppExecption):
    def __init__(self, detail):
        super().__init__(403, detail)

class NotFound(AppExecption):
    def __init__(self, detail):
        super().__init__(404, detail)
        


class LoginAlreadyExist(AppExecption):
    def __init__(self, detail):
        super().__init__(409, detail)


class NotValidData(AppExecption):
    def __init__(self, detail):
        super().__init__(422, detail)


        
        