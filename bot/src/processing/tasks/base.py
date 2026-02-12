from abc import ABC
from abc import abstractmethod


class BaseTask(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass