from src.core.infrastructures import rmq_broker
from src.handlers.create.event import OrderCreatedEvent

order_created_publisher = rmq_broker.broker.publisher(
    exchange=rmq_broker.exchange,
    routing_key="event.order.created",
    schema=OrderCreatedEvent,
)
