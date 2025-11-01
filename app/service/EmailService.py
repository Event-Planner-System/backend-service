from ..core.config import settings
from ..email_templates.EmailTemplateInterface import EmailTemplateInterface
from email.message import EmailMessage
import smtplib
from email.utils import formataddr

class EmailService:
    def __init__(self, template: EmailTemplateInterface):
        self.template = template

    def send_email(self, to_address: str, context: dict) -> None:
        subject = self.template.subject
        body = self.template.render(context)


        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = formataddr(("Event Planner System", settings.EMAIL_ADDRESS))
        msg['To'] = to_address
        msg.set_content(body)  

    
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  
            server.login(settings.EMAIL_ADDRESS, settings.EMAIL_APP_KEY)
            server.send_message(msg)

        print(f"Email sent to {to_address}")
