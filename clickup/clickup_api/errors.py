from requests import Response


class DatabaseNullValueError(Exception):
    def __init__(self, field, message='should not be NULL'):
        self.field = field
        self.message = field + ' ' + message
        super(DatabaseNullValueError, self).__init__(self.message)


class ApiRequestError(Exception):
    def __init__(self, request: Response):
        self.err = request.json()['err']
        self.code = request.json()['ECODE']
        self.message = self.err + ' \nError code: ' + self.code
        super(ApiRequestError, self).__init__(self.message)


class AuthTokenError(ApiRequestError):
    def __init__(self, request: Response):
        super(AuthTokenError, self).__init__('Error ' + request.json()['ECODE'] + ':' + request.json()['err'])


class TeamNotAuthorized(ApiRequestError):
    def __init__(self, request: Response):
        super(TeamNotAuthorized, self).__init__('Error ' + request.json()['ECODE'] + ':' + request.json()['err'])
