from .auth import router as auth_router
from .payment import router as payment_router
from .user import router as user_router
from .wallet import router as wallet_router

routers = [auth_router, payment_router, user_router, wallet_router]
