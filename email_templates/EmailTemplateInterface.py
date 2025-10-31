from abc import ABC, abstractmethod

class EmailTemplateInterface(ABC):
    @abstractmethod
    def set_subject(self, subject:str) -> None:
        pass
    
    @abstractmethod
    def set_body(self, body:str) -> None:
        pass   
    
    @abstractmethod
    def render(self, context:dict) -> str:
        pass