from abc import ABC
from abc import abstractmethod

#Для всех тасок, которые работают с базой
class PreparableTask(ABC):
    @abstractmethod
    async def prepare(self, connection):
        pass