from pydantic import BaseModel, EmailStr, Field, model_validator


class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    first_name: str | None = Field(default=None, max_length=150)
    last_name: str | None = Field(default=None, max_length=150)
    is_super_admin: bool | None = None
    is_venue_manager: bool | None = None
    is_attendee: bool | None = None
    tenant_name: str = Field(max_length=200)

    @model_validator(mode="after")
    def require_one_role(self):
        if not any([self.is_super_admin, self.is_venue_manager, self.is_attendee]):
            raise ValueError(
                "At least one role must be selected: is_super_admin, is_venue_manager, or is_attendee."
            )
        return self