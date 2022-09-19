class ConflictError(Exception):
    
    def __init__(self, message='A conflict error occured') -> None:
        self.messages = {'errors': message}
        super().__init__(message)

class NotFoundError(Exception):
    
    def __init__(self, message='A not-found error occured') -> None:
        self.messages = {'errors': message}
        super().__init__(message)

class AuthorizationError(Exception):
    
    def __init__(self, message='An authorization error occured') -> None:
        self.messages = {'errors': message}
        super().__init__(message)

class PermissionError(Exception):
    
    def __init__(self, message='A permission error occured') -> None:
        self.messages = {'errors': message}
        super().__init__(message)