from datetime import date, timedelta
from enum import Enum, StrEnum
from typing import Annotated, Any, Union

import httpx
import sqlalchemy as sa
from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, Field, field_validator

from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.shared_kernel.infra.camel_model import CamelModel

UserId = Annotated[str, ""]
CategoryIds = Annotated[list[int], []]
Ratings = Annotated[list[int], []]
SiteId = Annotated[str, ""]
StyleId = Annotated[int, 0]
OrderId = Annotated[str, ""]
OrganizationId = Annotated[str, ""]
OrganizationMemberId = Annotated[int, 0]
StyleVariantId = Annotated[int, 0]
StyleCollectionId = Annotated[str, ""]
HTTPClinet = Annotated[
    Union[httpx.AsyncClient, httpx.Client],
    httpx.AsyncClient,
]
Embedding = Annotated[list[float], []]


class MetadataVO(BaseModel):
    name: str
    type: str
    value: str

    @field_validator("value", mode="before")
    def value_validator(cls, v: str | list[str]) -> str:
        if isinstance(v, list):
            return "\n".join(v)
        return v


class FacetType(StrEnum):
    COLOR = "color"
    SIZE = "size"
    GENDER = "gender"
    CATEGORY = "category"
    FABRIC = "fabric"
    STYLE = "style"


class OrgRoleType(Enum):
    ROOT = 0
    ADMIN = 1
    BILLING = 2
    USER = 3


class Currency(StrEnum):
    USD = "USD"
    EUR = "EUR"
    KWR = "KRW"
    JYR = "JPY"


class PriceRage(CamelModel):
    start_price: str | None = None
    end_price: str | None = None
    currency: Currency = Currency.USD

    def between(self, c: Any):
        s = float(self.start_price)
        e = float(self.end_price)
        if s and e:
            return sa.and_(s <= c, c <= e)
        if s:
            return self.start_price <= c
        if e:
            return c <= e
        return True


class DateRange(CamelModel):
    start_date: date | None = Field(None)
    end_date: date | None = Field(None)

    def between(self, c: Any):
        s = self.start_date
        e = self.end_date + timedelta(days=1) if self.end_date else None
        if s and e:
            return sa.and_(s <= c, c <= e)
        if s:
            return self.start_date <= c
        if e:
            return c <= e
        return True

    @property
    def preve(self) -> "DateRange":
        if self.start_date is None or self.end_date is None:
            return DateRange()
        month_diff = self.__month_difference(self.start_date, self.end_date)
        start_date = self.start_date - relativedelta(months=month_diff) - relativedelta(days=1)
        start_date = start_date.replace(day=1)
        end_date = self.start_date - relativedelta(days=1)
        return DateRange(start_date=start_date, end_date=end_date)

    @classmethod
    def __month_difference(cls, start_date: date, end_date: date):
        year_diff = end_date.year - start_date.year
        month_diff = end_date.month - start_date.month
        total_month_diff = year_diff * 12 + month_diff
        return total_month_diff

    def __str__(self) -> str:
        if self.start_date is None or self.end_date is None:
            return ""
        return f"{self.start_date.strftime('%Y-%m-%d')} ~ {self.end_date.strftime('%Y-%m-%d')}"


class ReviewContentSchema(CamelModel):
    title: str | None = Field(default=None)
    text: str | None = Field(default=None)


class OrderStatus(StrEnum):
    pending = "PENDING"
    cancelled = "CANCELLED"
    failed = "FAILED"
    completed = "COMPLETED"


class PaymentMethod(StrEnum):
    credit_card = "CreditCard"
    toss = "Toss"
    kakaopay = "Kakaopay"
    naverpay = "Naverpay"
    mobilepay = "Mobilepay"
    payco = "Payco"
    bank_account = "BankAccount"


class PaymentStatus(StrEnum):
    pending = "PENDING"
    rejected = "REJECTED"
    completed = "COMPLETED"
    failed = "FAILED"


class NotificationStatus(StrEnum):
    pending = "PENDING"
    sent = "SENT"
    failed = "FAILED"
    cancelled = "CANCELLED"
