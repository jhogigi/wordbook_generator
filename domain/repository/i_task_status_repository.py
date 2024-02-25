from abc import ABCMeta, abstractclassmethod

from domain.entity.task_status_entity import TaskStatusEntity

class ITaskStatusRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def get_by_id(self, task_id: str) -> TaskStatusEntity:
        raise NotImplementedError()
