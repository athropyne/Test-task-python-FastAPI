from src.core.infrastructures import rmq_broker

product_quantities_calculated_publisher = rmq_broker.broker.publisher(
    exchange=rmq_broker.exchange,
    routing_key="event.order.products.product_quantities_calculated",
)

there_is_not_enough_product_publisher = rmq_broker.broker.publisher(
    exchange=rmq_broker.exchange,
    routing_key="event.order.products.not_enough_product"
)