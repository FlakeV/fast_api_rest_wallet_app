from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from app.schemas.auth import UserAdd
from app.services.user import UserService
import json

router = APIRouter(
    prefix="/api/v1/users",
)


@router.post("/")
async def create_user(body: UserAdd):
    new_user_dict = await UserService.create_user(body)
    print(new_user_dict)
    return JSONResponse(status_code=201, content=new_user_dict)


@router.get("/{user_id}")
async def read_users(user_id: int):
    return [
        {"username": "Rick"},
        {"username": "Morty"},
        {"username": "Beth"},
        {"username": "Summer"},
        {"username": "Beth"},
    ]
