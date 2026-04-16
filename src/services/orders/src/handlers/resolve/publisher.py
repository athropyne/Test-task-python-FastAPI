from src.core.infrastructures import rmq_broker

commit_order_publisher = rmq_broker.broker.publisher(
    exchange=rmq_broker.exchange,
    routing_key="event.order.commited",
)
reject_order_publisher = rmq_broker.broker.publisher(
    exchange=rmq_broker.exchange,
    routing_key="event.order.rejected",
)
