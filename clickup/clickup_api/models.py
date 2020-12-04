from .basic_classes import *
from .basic_classes import dict_update_by_options


class Team(DictBasedBasicClass):
    def __init__(self, base_dict: dict):
        self.id = None
        self.name = None
        self.color = None
        self.avatar = None
        super(Team, self).__init__(base_dict)

    def __str__(self):
        return self.name


class Status(DictBasedBasicClass):
    def __init__(self, json_object: dict):
        self.status = None
        self.color = None
        super().__init__(json_object)

    def __str__(self):
        return self.status


class BaseTask(DictBasedBasicClass):
    _TASK_URL = 'https://app.clickup.com/t/'

    def __init__(self, json_object: dict):
        self.id = str
        self.name = str
        self.status = Status
        self.url = str
        self.parent = None
        super().__init__(json_object)

    def __str__(self):
        return self.name


class Task(BaseTask):
    """ClickUp Task model"""

    def __init__(self, json_object: dict):
        super().__init__(json_object)
        self.subtasks = []

    def add_subtask(self, subtask):
        if not isinstance(subtask, SubTask):
            self.subtasks.append(SubTask(subtask))
        else:
            self.subtasks.append(subtask)


class SubTask(BaseTask):
    """SubTask model"""

    def __init__(self, json_object: dict):
        self.parent = str
        super(SubTask, self).__init__(json_object)

        self.parent_url = self._TASK_URL + self.parent


class AuthorizedUser(ModelClass, ModelInterface):
    """
    ClickUp AuthorizedUser
    """
    _NAME = 'user'
    _METHOD = Method.GET
    _URL = 'https://api.clickup.com/api/v2/user'

    def __init__(self, token):
        super().__init__(token)
        self.id = str
        self.username = str
        self.color = str
        self.profilePicture = str
        self._init_class_vars(self._NAME)

    def _init_class_vars(self, specify=None, **kwargs) -> None:
        request = self._make_request(specify)
        dict_update_by_options(self.__dict__, d_upd=self.__dict__, d_src=request)


class Teams(GroupsBasicClass):
    _URL = 'https://api.clickup.com/api/v2/team'
    _METHOD = Method.GET
    _NAME = 'teams'
    _SUB_CLASS = Team

    def __init__(self, token):
        self.teams = None
        super(Teams, self).__init__(token)


class Tasks(BasicMultipleModelClass, ModelInterface):
    _URL = 'https://api.clickup.com/api/v2/team/{request_id}/task'
    _REQUEST_ID_REQUIRED = True
    _METHOD = Method.GET
    _NAME = 'tasks'
    _MODEL_PARENT_FIELD_NAME = 'team_id'

    def __init__(self, token, user_id: str, filters=None):
        super().__init__(token)
        if not filters:
            self._REQUEST_PARAMS = filters
        else:
            self._REQUEST_PARAMS = {
                'assignees[]': [user_id],
                'subtasks': True,
                'order_by': 'updated'
            }
        self.sub_tasks = {}
        self._init_request_id()
        self._init_class_vars(Tasks._NAME)
        # self._sort_tasks() sorting, putting tasks inside subtasks

    def _init_class_vars(self, specify=None, **kwargs):
        request = self._make_request(specify)
        for task in request:
            if not task['parent']:
                self.sub_tasks.update({task['id']: Task(task)})
            else:
                cur_parent_task_id = task['parent']
                if cur_parent_task_id in self.sub_tasks:
                    task[cur_parent_task_id].add_subtask(task)
                else:
                    self.sub_tasks.update({task['id']: SubTask(task)})

    def _sort_tasks(self):
        delete_arr = []
        for task in self.sub_tasks.values():
            if task.parent and (task.parent in self.sub_tasks):
                self.sub_tasks[task.parent].add_subtask(task)
                delete_arr.append(task.id)

        for to_delete in delete_arr:
            self.sub_tasks.pop(to_delete)
