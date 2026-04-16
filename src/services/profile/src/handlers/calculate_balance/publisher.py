from src.core.infrastructures import rmq_broker
from src.handlers.event import OrderCreatedEvent

no_enough_money_publisher = rmq_broker.broker.publisher(
    exchange=rmq_broker.exchange,
    routing_key="event.order.profile.not_enough_money",
    schema=OrderCreatedEvent,
)

money_has_been_debited_publisher = rmq_broker.broker.publisher(
    exchange=rmq_broker.exchange,
    routing_key="event.order.profile.money_has_been_debited",
    schema=OrderCreatedEvent,
)