from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class RegisteredUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    first_name: str | None
    last_name: str | None
    is_super_admin: bool
    tenant_name: str

class RegisterUserResponse(BaseModel):
    status: str
    message: str
    user: RegisteredUser


