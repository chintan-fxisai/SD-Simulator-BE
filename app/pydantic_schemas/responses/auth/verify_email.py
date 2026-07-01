from pydantic import BaseModel


class VerifyEmailResponse(BaseModel):
    status: str
    detail: str
