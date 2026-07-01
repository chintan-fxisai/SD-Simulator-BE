from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.databse import get_async_db
from app.pydantic_schemas.requests.auth.register import RegisterUserRequest
from app.pydantic_schemas.responses.auth.register import RegisterUserResponse
from app.pydantic_schemas.responses.auth.verify_email import VerifyEmailResponse
from app.services.auth.register import register_user_service
from app.services.auth.verify_email import verify_registration_email_service


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=RegisterUserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register_user(
    payload: RegisterUserRequest,
    db: AsyncSession = Depends(get_async_db),
):
    return await register_user_service(payload=payload, db=db)


@router.get(
    "/verify-email",
    response_model=VerifyEmailResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify registered user email",
)
async def verify_registration_email(
    token: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_async_db),
):
    return await verify_registration_email_service(token=token, db=db)
