from service.EmailService import EmailService
from email_templates.RegisterationTemplate import RegistrationTemplate

template = RegistrationTemplate()

email_service = EmailService(template)
context = {"name": "malouka", "app_name": "Event planner"}

email_service.send_email("malaksherifmohamed99@gmail.com", context)