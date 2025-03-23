from fastapi import status, HTTPException, Response

from api.request import LoginRequestSchema, CreateUserRequestSchema, UpdateUserRequestSchema
from app.services.abstract import AbstractService
from core.config import config
from core.db.dao import UserDAO
from core.db.models import UserModel
from core.db.session import session


class UserService(AbstractService):

    @classmethod
    async def login(cls, response: Response, body: LoginRequestSchema):
        user = await cls.get_user_by_filters(email=body.email)
        cls._compare_passwords(
            email=body.email,
            user_hashed_password=user.password,
            password_from_request=body.password
        )
        response.set_cookie(
            key="session",
            value=cls._generate_session_cookie,
            httponly=True,
            secure=False,
            expires=config.security.session_expire_minutes
        )

    @classmethod
    async def create_user(cls, body: CreateUserRequestSchema) -> UserModel:
        if await cls.get_user_by_filters(email=body.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email {body.email} already exist"
            )
        body.password = cls._hash_password(body.password, body.email)
        user = UserModel(**body.model_dump())

        async with session() as transaction:
            try:
                user = await UserDAO(transaction).create_user(user)
                await transaction.commit()
            except Exception:
                await transaction.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create user"
                )
        return user

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> UserModel:
        if user := await cls.get_user_by_filters(id=user_id):
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Failed to find user by id {user_id}"
            )

    @classmethod
    async def get_all_users(cls, limit: int, offset: int) -> list[UserModel]:
        async with session() as transaction:
            users = await UserDAO(transaction).get_all_users(limit=limit, offset=offset)
            return users

    @classmethod
    async def delete_user(cls, user_id: int):
        async with session() as transaction:
            await UserDAO(transaction).delete_user(user_id)

    @classmethod
    async def update_user(cls, user_id: int, body: UpdateUserRequestSchema) -> UserModel:
        if await cls.get_user_by_filters(email=body.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {body.email} already exist"
            )
        user = await cls.get_user_by_filters(id=user_id)
        if user.email == body.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User already have email {body.email}"
            )
        if body.password:
            body.password = cls._hash_password(password=body.password, email=user.email)
        body = body.model_dump(exclude_none=True)
        for field, value in body.items():
            setattr(user, field, value)
        async with session() as transaction:
            try:
                transaction.add(user)
                await transaction.commit()
                return user
            except Exception:
                await transaction.rollback()

    @classmethod
    def _generate_session_cookie(cls):
        ...
