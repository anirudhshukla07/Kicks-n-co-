from pydantic import BaseModel, EmailStr


class NewsletterRequest(BaseModel):
    email: EmailStr


class MessageResponse(BaseModel):
    message: str
