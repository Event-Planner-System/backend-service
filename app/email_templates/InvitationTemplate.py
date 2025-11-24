from ..email_templates.EmailTemplateInterface import EmailTemplateInterface

class InvitationTemplate(EmailTemplateInterface):
    def __init__(self):
        self.subject = "Event Invitation!"
        self.body = "Hello {name}, you are invited to join {event_name} event at {app_name} as {role}!\nPlease check your dashboard for more details.🎉"
        
    def set_subject(self, subject:str) -> None:
        self.subject = subject
        pass
    
    def set_body(self, body:str) -> None:
        self.body = body
        pass   
    
    def render(self, context:dict) -> str:
        self.body = self.body.format(**context)
        return self.body