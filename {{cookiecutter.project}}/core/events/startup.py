async def startup_event():
    from core.db.session import Base, engines
    async with engines["writer"].begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
