import jwt
from fastapi import Response, HTTPException, status

from api.request import LoginRequestSchema
from app.services.abstract import AbstractService
from core.config import config


class AuthService(AbstractService):
    @classmethod
    async def login(cls, response: Response, body: LoginRequestSchema) -> dict:
        user = await cls.get_user_by_filters(email=body.email)
        cls._compare_passwords(
            email=body.email,
            user_hashed_password=user.password,
            password_from_request=body.password
        )
        response.set_cookie(
            key="session",
            value=cls._generate_session_cookie(user_id=user.id, role=user.role),
            httponly=True,
            secure=False,
            expires=config.security.session_expire_minutes
        )
        return {"result": "OK"}

    @classmethod
    def _compare_passwords(
            cls,
            email: str,
            user_hashed_password: str,
            password_from_request: str
    ) -> None:
        if user_hashed_password != cls._hash_password(email=email, password=password_from_request):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password or email"
            )

    @classmethod
    def _generate_session_cookie(cls, user_id: int, role: str) -> str:
        data = {"id": user_id, "role": role}
        return jwt.encode(payload=data, algorithm="HS256", key=config.security.secret_key)
