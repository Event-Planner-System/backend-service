import random
from service.EmailService import EmailService
from email_templates.VerificationCodeTemplate import VerificationTemplate

def generate_verification_code() -> str:
    return f"{random.randint(100000, 999999)}"

def send_verification_code(to_email: str, username: str) -> None:
    pass