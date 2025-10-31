from core import EMAIL_ADDRESS, EMAIL_APP_KEY
from email_templates.EmailTemplateInterface import EmailTemplateInterface
import smtplib
class EmailService:
    def __init__(self, template:EmailTemplateInterface):
        self.template = template

    def send_email(self, to_address:str, context:dict) -> None:
        subject = self.template.subject
        body = self.template.render(context)
        email_text = f"Subject: {subject}\n\n{body}"

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_APP_KEY)
            server.sendmail(EMAIL_ADDRESS, to_address, email_text)
            print(f"Email sent to {to_address}")