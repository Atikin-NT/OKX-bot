from okx.account import Account
import time
from abc import ABC, abstractmethod

class BaseLogic(ABC):

    @abstractmethod
    def parse(self) -> None:
        pass

    @abstractmethod
    def dicision_making(self) -> bool:
        pass

    @abstractmethod
    def dicision_execution(self) -> None:
        pass
    
