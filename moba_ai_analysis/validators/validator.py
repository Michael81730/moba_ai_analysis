from abc import ABC, abstractmethod

class Validator(ABC):
    name = ""

    @abstractmethod
    def validate(self, value):
        pass
    
