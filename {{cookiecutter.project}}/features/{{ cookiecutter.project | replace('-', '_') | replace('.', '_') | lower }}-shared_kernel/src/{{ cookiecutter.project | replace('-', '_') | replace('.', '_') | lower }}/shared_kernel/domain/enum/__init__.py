from enum import StrEnum  # noqa: F401


class ExpenseType(StrEnum):
    INCOME = "income"
    EXPENSE = "expense"


class Gender(StrEnum):
    M = "M"
    F = "F"


class ApplicationMode(StrEnum):
    devel = "DEV"
    production = "PROD"
    admin = "ADMIN"
    test = "test"
