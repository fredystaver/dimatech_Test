from contextvars import ContextVar, Token
from typing import Union

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import config

session_context: ContextVar[str] = ContextVar("session_context")

def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)

engine = create_async_engine(
    config.postgres.database_url,
    pool_recycle=3600,
    pool_size=config.postgres.pool_size,
    max_overflow=config.postgres.max_overflow,
    echo=config.postgres.echo
)

async_session_factory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_session_context,
)

Base = declarative_base()
