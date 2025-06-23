from {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }}.shared_kernel.infra.fastapi.exception_handlers.base import BaseMsgException


class ExpenseException(BaseMsgException):
    """
    Base exception for all expense-related errors.
    """

    error: str = ""
    message: str = ""
    code: int = 500


class ExpenseNotAnalyzedException(ExpenseException):
    """
    Exception raised when an expense has not been analyzed.
    """

    error: str = "ExpenseNotAnalyzed"
    message = "analyzed expense count is 0, please analyze new message."
    code: int = 404


class ExpenseNotFoundException(ExpenseException):
    """
    Exception raised when an expense is not found.
    """

    error: str = "ExpenseNotFound"
    message: str = "Expense not found."
    code: int = 404
