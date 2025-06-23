from typing import TypeVar

EntityType = TypeVar("EntityType", bound="Entity")


class Entity:
    pass


class AggregateRoot(Entity):
    pass
