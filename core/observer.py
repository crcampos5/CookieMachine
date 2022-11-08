from __future__ import annotations
from abc import ABC, abstractmethod
#from core.subject import Subject

class Observer(ABC):

    @abstractmethod
    def update(self, subject) -> None:
        pass
