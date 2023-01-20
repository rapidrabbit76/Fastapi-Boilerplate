from typing import Union
from uuid import uuid4
from fastapi.requests import Request


from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
)
from core.db.session import (
    set_session_context,
    reset_session_context,
    async_session_factory,
    get_session_context,
)


class SQLAlchemyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)
        try:
            session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
                session_factory=async_session_factory,
                scopefunc=get_session_context,
            )
            request.state.db = session()
            response = await call_next(request)
        except Exception as e:
            raise e
        finally:
            await session.remove()
            reset_session_context(context=context)

        return response


# async def db_session_middleware(request: Request, call_next):
#     request_id = str(uuid1())

#     ctx_token = _request_id_ctx_var.set(request_id)
#     path_params = get_path_params_from_request(request)

#     request.state.organization = "default"
#     schema_engine = engine.execution_options(
#         schema_translate_map={
#             None: "dispatch_organization_default",
#         }
#     )
#     try:
#         session = scoped_session(
#             sessionmaker(bind=schema_engine), scopefunc=get_request_id
#         )
#         request.state.db = session()
#         response = await call_next(request)
#     except Exception as e:
#         raise e from None
#     finally:
#         request.state.db.close()

#     _request_id_ctx_var.reset(ctx_token)
#     return response
