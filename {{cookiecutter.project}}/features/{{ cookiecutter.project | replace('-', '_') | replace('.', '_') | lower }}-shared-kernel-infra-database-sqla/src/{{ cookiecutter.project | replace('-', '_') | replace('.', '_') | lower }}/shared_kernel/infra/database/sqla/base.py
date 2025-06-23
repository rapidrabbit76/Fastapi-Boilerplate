from sqlalchemy import MetaData
from sqlalchemy.orm import registry, declarative_base, declared_attr
import re

metadata = MetaData()
reg = registry(metadata=metadata)


class TableNamePrefixMixin:
    @staticmethod
    def camel_to_snake(name: str) -> str:
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    @declared_attr
    def __tablename__(self) -> str:
        return f"{{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}_{self.camel_to_snake(self.__name__.lower())}"


Base = declarative_base(metadata=metadata)
