from fastapi import FastAPI
from starlette_admin.contrib.sqla import Admin, ModelView

from services.user.models import User
from core.db.session import engines
from .auth import AdminAuthProvider


def admin_app(app: FastAPI) -> FastAPI:
    fastapi_admin = Admin(
        engine=engines["writer"],
        title="{{cookiecutter.project}}",
        auth_provider=AdminAuthProvider(),
    )
    fastapi_admin.add_view(ModelView(User))
    fastapi_admin.mount_to(app)
    return app
