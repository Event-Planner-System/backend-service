from ..email_templates.EmailTemplateInterface import EmailTemplateInterface

class RegistrationTemplate(EmailTemplateInterface):
    def __init__(self):
        self.subject = "Your account has been created!"
        self.body = "Hello {name}, thanks for registering at {app_name}!\nEnjoy our services!❤️"
        
    def set_subject(self, subject:str) -> None:
        self.subject = subject
        pass
    
    def set_body(self, body:str) -> None:
        self.body = body
        pass   
    
    def render(self, context:dict) -> str:
        self.body = self.body.format(**context)
        return self.body