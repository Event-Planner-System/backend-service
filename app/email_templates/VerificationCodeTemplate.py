from email_templates.EmailTemplateInterface import EmailTemplateInterface

class VerificationCodeTemplate(EmailTemplateInterface):
    def __init__(self):
        self.subject = "Verfiy Your Account"
        self.body = "Hello {name}, this is your verification code: {code}. It will expire in {expiry_minutes} minutes."
        
    def set_subject(self, subject:str) -> None:
        self.subject = subject
        pass
    
    def set_body(self, body:str) -> None:
        self.body = body
        pass   
    
    def render(self, context:dict) -> str:
        self.body = self.body.format(**context)
        return self.body