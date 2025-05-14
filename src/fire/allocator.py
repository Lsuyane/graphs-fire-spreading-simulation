from abc import ABC, abstractmethod
from events import Event

class Allocator(ABC):
    @abstractmethod
    def notify(self, event: Event):
        pass

    @abstractmethod
    def notify_and_update(self, event: Event):
        pass