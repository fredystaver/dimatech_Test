import jwt
from fastapi import Request, HTTPException, status

from core.config import config
from core.db.models import UserModel


async def check_permission(request: Request):
    cookie_jwt = request.cookies.get("session")
    if not cookie_jwt:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    try:
        cookie_data = jwt.decode(cookie_jwt, key=config.security.secret_key, algorithms=["HS256"])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Unknown error'
        )
    role = cookie_data.get('role')
    if role != UserModel.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission debued"
        )
