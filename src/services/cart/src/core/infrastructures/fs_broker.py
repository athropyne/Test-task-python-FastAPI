import functools
from datetime import datetime, timedelta
from decimal import Decimal
from typing import (
    Type,
    Sequence,
    Any,
    Coroutine,
    Callable,
)

from aio_pika import Message
from faststream._internal.basic_types import StandardDataclass
from faststream.rabbit import RabbitExchange, ExchangeType, RabbitQueue
from faststream.rabbit.fastapi import RabbitBroker
from faststream.rabbit.publisher import RabbitPublisher
from pydantic import BaseModel


class RMQBroker:
    def __init__(self,
                 login: str,
                 password: str,
                 host: str,
                 port: int):
        self.url = f"amqp://{login}:{password}@{host}:{port}"
        self.broker: Type[RabbitBroker] = RabbitBroker(self.url)
        self.exchange = RabbitExchange(
            name="events",
            type=ExchangeType.TOPIC,
            durable=True
        )

    async def publish(
            self,
            message: Message | bool | bytes | bytearray | float | int | str | None | Decimal | datetime | StandardDataclass |
                     dict[str, Any] | Sequence[Any] = None,
            queue: RabbitQueue | str = "",
            *,
            routing_key: str = "",
            mandatory: bool = True,
            immediate: bool = False,
            timeout: int | float | None = None,
            persist: bool = False,
            reply_to: str | None = None,
            correlation_id: str | None = None,
            headers: dict[str, bool | bytes | bytearray | Decimal | list[Any] | dict[
                str, Any] | float | int | None | str | datetime] | None = None,
            content_type: str | None = None,
            content_encoding: str | None = None,
            expiration: int | datetime | float | timedelta | None = None,
            message_id: str | None = None,
            timestamp: int | datetime | float | timedelta | None = None,
            message_type: str | None = None,
            user_id: str | None = None,
            priority: int | None = None):
        return await self.broker.publish(
            message=message,
            queue=queue,
            exchange=self.exchange,
            routing_key=routing_key,
            mandatory=mandatory,
            immediate=immediate,
            timeout=timeout,
            persist=persist,
            reply_to=reply_to,
            correlation_id=correlation_id,
            headers=headers,
            content_type=content_type,
            content_encoding=content_encoding,
            expiration=expiration,
            message_id=message_id,
            timestamp=timestamp,
            message_type=message_type,
            user_id=user_id,
            priority=priority,
        )

    async def start(self):
        await self.broker.start()
        await self.broker.declare_exchange(self.exchange)

    async def __call__(self):
        return self


    def produce(self, func: Callable):
        def decorator(publisher: RabbitPublisher, event_model_type: Type[BaseModel]):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                call_result = await func(*args, **kwargs)
                event_model = event_model_type(**call_result.model_dump()).model_dump()
                publish_event = await publisher.publish(event_model)
                return call_result
            return wrapper
        return decorator

