class ValueObjectEnumError(Exception):
    def __str__(self):
        return "Value Object got invalid value."


class BaseMsgException(Exception):
    error: str = ""
    message: str = ""
    code: int = 500

    def __str__(self):
        return self.message

    @classmethod
    def create(cls, e: Exception) -> "BaseMsgException":
        model = cls()
        model.error = str(e)
        model.message = getattr(e, "message")
        model.code = getattr(e, "code")
        return model
