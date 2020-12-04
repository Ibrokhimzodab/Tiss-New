from typing import Optional
from ..models import ClickUpUserId
import requests
from enum import Enum
from abc import abstractmethod, ABC
from .errors import ApiRequestError, AuthTokenError, TeamNotAuthorized

_ERRORS = {

    'AuthTokenError': ('OAUTH_017', 'OAUTH_019', 'OAUTH_021', 'OAUTH_025', 'OAUTH_077'),
    'TeamNotAuthorized': ('OAUTH_056',)
}


def make_params(**kwargs):
    return kwargs


def dict_update_by_options(params: dict, d_upd: dict, d_src: dict) -> None:
    """
    Updates d_upd params according to 'params' of params to include which included in d_src.
    d_src, d_upd - Dict objects
    o - List object
    """
    for param, sub_class in params.items():
        if sub_class:
            d_upd.update({param: sub_class(d_src[param])})
        else:
            d_upd.update({param: d_src[param]})


class Method(Enum):
    """Request methods enum"""
    GET = 'GET'
    POST = 'POST'

    def upper(self):
        return self._value_.upper()


class DictBasedBasicClass(ABC):
    def __init__(self, base_dict: dict):
        dict_update_by_options(self.__dict__, self.__dict__, base_dict)

    @abstractmethod
    def __str__(self) -> str:
        """Should return object transformed in str"""


class BasicClass:
    """BasicClass for models.
    TOKEN - API authorization token
    METHOD - method used for making requests
    URL - request url
    REQUEST_PARAMS - params for requests example:
        'https://api.clickup.com/api/v2/task/task_id/comment/?custom_task_ids=&team_id=' after params after ?
    """
    _TOKEN = None
    _METHOD = None
    _URL = None
    _REQUEST_PARAMS = None

    def _make_request(self, specify=None):
        """
        :param specify: specify tag from gotten json
        :return: json object
        """
        request = requests.request(method=self._METHOD,
                                   url=self._URL,
                                   **make_params(headers={'Authorization': self._TOKEN},
                                                 params=self._REQUEST_PARAMS))
        if request.status_code == 401:
            err_code = request.json()['ECODE']
            if err_code in _ERRORS['AuthTokenError']:
                raise AuthTokenError(request)
            elif err_code in _ERRORS['TeamNotAuthorized']:
                raise TeamNotAuthorized(request)
            raise ApiRequestError(request)

        if specify:
            return request.json()[specify]
        return request.json()


class ModelInterface(ABC):

    @abstractmethod
    def _init_class_vars(self, **kwargs):
        """Used to init variables dynamically filled with request data"""


class ModelClass(BasicClass):

    def __init__(self, token):
        ModelClass._TOKEN = token


class BasicMultipleModelClass(ModelClass):
    """
    Basic class for objects with dynamic multiple content.

    MODEL_PARENT_FIELD_NAME - field name in clickup.models ClickUpUserIds model which this class depends on
    REQUEST_ID - id from parent class to make request, can be None if not required by REQUEST_ID_REQUIRED
    REQUEST_ID_REQUIRED - bool variable shows is parent id required
    """
    _MODEL_PARENT_FIELD_NAME = None
    _REQUEST_ID = None
    _REQUEST_ID_REQUIRED = False

    def __init__(self, token):
        super().__init__(token)

    @classmethod
    def _get_request_ids_by_db(cls) -> Optional[str]:
        """If failed rises ClickUpUserId.DesNotExist"""
        return ClickUpUserId.objects.get(auth_token=cls._TOKEN).__getattribute__(cls._MODEL_PARENT_FIELD_NAME)

    @classmethod
    def _init_request_id(cls) -> None:
        if cls._REQUEST_ID_REQUIRED and cls._MODEL_PARENT_FIELD_NAME:
            cls._REQUEST_ID = cls._get_request_ids_by_db()
            cls._URL.format(requset_id=cls._REQUEST_ID)


class GroupsBasicClass(BasicMultipleModelClass, ModelInterface):
    """Basic class for objects with multiple objects."""
    _NAME = None
    _SUB_CLASS = None

    def __init__(self, token):
        super().__init__(token)
        self._init_request_id()
        self._init_class_vars(self._NAME)

    def _init_class_vars(self, specify=None, **kwargs) -> None:
        request = self._make_request(specify)
        self.__setattr__(self._NAME, list())
        for dict_element in request:
            self.__dict__.get(self._NAME).append(self._SUB_CLASS(dict_element))
