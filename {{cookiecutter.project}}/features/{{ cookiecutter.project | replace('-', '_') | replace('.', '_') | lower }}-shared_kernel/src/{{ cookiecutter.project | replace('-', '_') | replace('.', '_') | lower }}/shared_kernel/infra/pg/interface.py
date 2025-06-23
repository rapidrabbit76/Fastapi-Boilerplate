from dataclasses import dataclass
import abc


@dataclass(slots=True, kw_only=True, init=True)
class PaymentGateway(abc.ABC):
    @abc.abstractmethod
    async def payment(self, *args, **kwargs):
        raise NotImplementedError
