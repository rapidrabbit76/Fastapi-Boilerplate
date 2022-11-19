from abc import ABC, abstractmethod
from typing import List, Type
from datetime import datetime
from fastapi import Request, Depends
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase
from app.user import UserService
from core.exceptions import (
    CustomException,
    UnauthorizedException,
    AdminUnauthorizedException,
)


class BasePermission(ABC):
    exception: Exception = CustomException

    def __init__(self, svc: UserService) -> None:
        super().__init__()
        self.svc = svc

    @abstractmethod
    async def has_permission(self, request: Request) -> bool:
        pass


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        return request.user.id is not None


class IsAdmin(BasePermission):
    exception = AdminUnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        user_id = request.user.id
        if not user_id:
            return False
        result = await self.svc.is_admin(user_id=user_id)
        return result


class IsActivated(BasePermission):
    exception = AdminUnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        user_id = request.user.id
        if not user_id:
            return False
        is_admin = await self.svc.is_admin(user_id=user_id)
        if is_admin:
            return True
        # 1. Permission key expired time Check : permission.expired_at <= datetime.now()
        # 2. request.url to demo id convert
        # 3. demo_id in permission.demos check
        return True

    async def is_admin(self) -> bool:
        return True

    async def is_expired(self, key: str) -> bool:
        return False

    async def is_permission(self, demo_id: str, user_id: int) -> bool:
        return False


class AllowAll(BasePermission):
    async def has_permission(self, request: Request) -> bool:
        return True


class PermissionDependency(SecurityBase):
    def __init__(self, permissions: List[Type[BasePermission]]):
        self.permissions = permissions
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__

    async def __call__(
        self,
        request: Request,
        svc: UserService = Depends(),
    ):
        for permission in self.permissions:
            cls = permission(svc)
            if not await cls.has_permission(request=request):
                raise cls.exception
