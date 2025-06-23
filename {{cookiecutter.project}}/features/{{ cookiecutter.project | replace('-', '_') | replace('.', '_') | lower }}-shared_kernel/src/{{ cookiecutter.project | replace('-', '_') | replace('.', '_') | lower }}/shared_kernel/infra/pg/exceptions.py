from typing import Any


class PaymentGatewayException(Exception):
    code: Any
    message: str
