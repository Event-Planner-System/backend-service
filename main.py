from fastapi import FastAPI
from api.AuthAPI import router as auth_router


app = FastAPI(
    title="User Management API",
    description="FastAPI + MongoDB example with authentication",
    version="1.0.0"
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])


@app.get("/")
async def root():
    return {"message": "User Management Service is running."}
# from service.EmailService import EmailService
# from email_templates.RegisterationTemplate import RegistrationTemplate

# template = RegistrationTemplate()

# email_service = EmailService(template)
# context = {"name": "malouka", "app_name": "Event planner"}

# email_service.send_email("malaksherifmohamed99@gmail.com", context)
