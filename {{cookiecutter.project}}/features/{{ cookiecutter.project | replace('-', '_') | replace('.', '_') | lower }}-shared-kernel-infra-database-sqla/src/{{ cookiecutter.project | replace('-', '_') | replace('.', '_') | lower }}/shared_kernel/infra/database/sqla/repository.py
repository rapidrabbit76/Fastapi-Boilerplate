from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.shared_kernel.domain.entity import EntityType


class RDBRepository:
    @staticmethod
    def add(session, instance: EntityType):
        return session.add(instance)

    @staticmethod
    async def delete(session, instance: EntityType):
        return await session.delete(instance)

    @staticmethod
    async def commit(session):
        return await session.commit()


class RDBReadRepository:
    pass
