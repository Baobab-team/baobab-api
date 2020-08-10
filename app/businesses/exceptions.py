from app.consts import DEFAULT_EXCEPTION_MESSAGE, MESSAGE_CONFLICT, MESSAGE_ENTITY_NOT_FOUND


class BaseException(Exception):
    status_code = 400

    def __init__(self, message=None, status_code=None):
        Exception.__init__(self, message)
        if status_code is not None:
            self.status_code = status_code

    @property
    def message(self):
        return DEFAULT_EXCEPTION_MESSAGE if self.message is None else self.message

    @property
    def code(self):
        return self.status_code

    def to_dict(self):
        return {'message': self.message, 'code': self.status_code}


class EntityNotFoundException(BaseException):
    status_code = 404
    message = MESSAGE_ENTITY_NOT_FOUND


class ConflictException(BaseException):
    status_code = 409
    message = MESSAGE_CONFLICT
