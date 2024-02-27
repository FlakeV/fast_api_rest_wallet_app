from app.configuration.routes.routes import Routes
from app.api.user import router as user_router
from app.api.auth import router as auth_router

__routers__ = Routes(
    routers=(
        auth_router,
        user_router,
    )
)
