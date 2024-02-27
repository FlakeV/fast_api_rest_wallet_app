from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas.auth import UserAdd, Token, User
from ..services.auth import AuthService, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign-in", response_model=Token, description="Register new user")
async def sign_in(user_data: UserAdd, auth_service: AuthService = Depends()):
    return await auth_service.register_user(user_data)


@router.post("/sign-up", response_model=Token, description="Login user")
async def sign_up(
    from_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),
):
    return await auth_service.authenticate_user(from_data.username, from_data.password)


@router.get("/user")
async def get_users(user: User = Depends(get_current_user)):
    return user
