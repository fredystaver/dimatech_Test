from hashlib import sha512

from core.config import config
from core.db.dao import UserDAO
from core.db.models import UserModel
from core.db.session import session


class AbstractService:
    @classmethod
    async def get_user_by_filters(cls, **filters) -> UserModel | None:
        async with session() as transaction:
            return await UserDAO(transaction).get_user_by_filters(**filters)

    @classmethod
    def _hash_password(cls, password: str, email: str) -> str:
        hasher = sha512()
        hasher.update(
            (password + config.security.password_salt + email).encode("utf-8")
        )
        return hasher.hexdigest()
