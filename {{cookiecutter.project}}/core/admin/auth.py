import core.db.session
from fastapi import Request, Response
from starlette_admin import BaseAdmin as Admin
from starlette_admin.auth import AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed
from sqlalchemy import select, or_, and_
from core.db import session
from services.user.models import User


users = {
    "admin": ["admin"],
}


class AdminAuthProvider(AuthProvider):
    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:

        query = select(User).where(
            and_(
                User.email == username,
                User.password == password,
            ),
        )
        result = await session.execute(query)
        user = result.scalars().first()
        if not user:
            raise LoginFailed("Invalid username or password")

        if not user.is_admin:
            raise LoginFailed(f"Invalid permission")

        response.set_cookie(
            key="user",
            value=username,
        )
        return response

    async def is_authenticated(self, request) -> bool:
        if "user" in request.cookies:
            email = request.cookies.get("user")
            query = select(User).where(
                and_(User.email == email, User.is_admin),
            )
            result = await session.execute(query)
            user = result.scalars().first()
            return user != None
        return False

    async def logout(self, request: Request, response: Response):
        response.delete_cookie(
            "user",
        )
        return response
