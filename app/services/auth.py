from datetime import datetime

from asyncpg import UniqueViolationError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.hash import bcrypt
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..configuration.settings import settings
from ..database.db import get_session
from ..database.models import User as UserModel
from ..schemas.auth import User, Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign-in/")


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return AuthService.verify_token(token)


class AuthService:

    @classmethod
    async def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    async def get_password_hash(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    async def verify_token(cls, token: str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
            )
        except JWTError:
            raise exception from None

        user_data = payload.get("user")
        try:
            user = User.parse_obj(user_data)
        except TypeError:
            raise exception from None
        return user

    @classmethod
    async def create_token(cls, user: UserModel) -> Token:
        user_data = User.from_orm(user)
        now = datetime.utcnow().timestamp()
        payload = {
            "sub": now,
            "iat": now,
            "exp": now + settings.jwt_expiration,
            "user": user_data.dict(),
        }
        token = jwt.encode(
            payload, settings.jwt_secret, algorithm=settings.jwt_algorithm
        )

        return Token(access_token=token)

    def __init__(self, session=Depends(get_session)):
        self.session = session

    async def register_user(self, user: User) -> Token:
        new_user = UserModel(
            username=user.username,
            email=user.email,
            password_hash=await self.get_password_hash(user.password),
            phone=user.phone,
        )
        try:
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
            return await self.create_token(new_user)
        except IntegrityError:
            raise HTTPException(
                status_code=400, detail=f"User with {user.email} email already exists"
            )

    async def authenticate_user(self, username: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        stmt = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(stmt)
        user = result.first()[0]
        if not user:
            raise exception

        if not await self.verify_password(password, user.password_hash):
            raise exception

        token = await self.create_token(user)
        return token
