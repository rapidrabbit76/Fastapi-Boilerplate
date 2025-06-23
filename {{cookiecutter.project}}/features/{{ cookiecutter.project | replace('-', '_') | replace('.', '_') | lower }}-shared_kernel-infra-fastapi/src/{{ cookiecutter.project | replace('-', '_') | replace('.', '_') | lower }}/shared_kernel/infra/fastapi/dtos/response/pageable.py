from typing import Any, Generic, List, Sequence, TypeVar, TYPE_CHECKING
from pydantic import BaseModel, computed_field
from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.shared_kernel.infra.camel_model import CamelModel, Field

if TYPE_CHECKING:
    from ..request.pageable import Pageable


T = TypeVar("T")


class PaginationList(list[T]):
    total: int | None = None
    metadata: Any | None = None

    @classmethod
    def build(
        cls,
        data: List[T] | Sequence[T],
        total: int | None = None,
        metadata: Any | None = None,
    ):
        model = cls(data)
        model.total = total
        model.metadata = metadata
        return model


class PageMeta(CamelModel):
    page: int
    size: int
    total: int | None = Field(default=None)

    @computed_field
    def total_page(self) -> int | None:
        if self.total is None:
            return None
        total_page = self.total // self.size
        if self.total % self.size > 0:
            total_page += 1
        return total_page

    @computed_field
    def offset(self) -> int:
        return (self.page - 1) * self.size


class PaginationResponse(BaseModel, Generic[T]):
    meta: PageMeta = Field()
    items: List[T] = Field(default_factory=list)

    @classmethod
    def build(cls, data: PaginationList[T] | list[T], pageable: "Pageable"):
        paging = PageMeta(
            page=pageable.page,
            size=pageable.size,
            total=data.total if hasattr(data, "total") else None,
        )
        metadata = data.metadata if hasattr(data, "metadata") else None
        return PaginationResponse(items=data, meta=paging, metadata=metadata)
