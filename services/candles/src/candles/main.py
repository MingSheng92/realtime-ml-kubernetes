# perform stateful transformation with quixstream
from loguru import logger
from quixstreams import Application


def init_candle():
    pass


def update_candle(candle, trade):
    pass


def run(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    candle_sec: int,
):
    """
    Transforms a stream of input trades into a stream of output candles.
    In 3 steps:
    - ingest trades from kafka_input_topic
    - transform trades into candles
    - produce candles to kafka_output_topic

    Args:
        kafka_broker_address (str): Kafka broker address
        kafka_input_topic (str): Kafka input topic
        kafka_output_topic (str): Kafka output topic
        kafka_consumer_group (str): Kafka consumer group name
        candle_sec (int): Candle duration in seconds

    Returns:
        None
    """
    app = Application(
        broker_address=kafka_broker_address, consumer_group=kafka_consumer_group
    )

    # input topic
    trades_topic = app.topic(kafka_input_topic, value_deserializer='json')
    # output topic
    candles_topic = app.topic(kafka_output_topic, value_serializer='json')

    # ingest trades from topic, create streaming dataframe connected to
    # input kafka topic
    sdf = app.dataframe(topic=trades_topic)

    # test dry run
    sdf = sdf.update(lambda message: logger.info(f'Input: {message}'))

    # step 3 - push data to kafka
    sdf = sdf.to_topic(candles_topic)

    # aggregate trades into candles using tumbling windows

    # sdf = (
    #     # degine tumbling windows of 10 minutes
    #     sdf.tumbling_window(timedelta(seconds=candle_sec))
    #     # create a reduce aggregation with a "reducer" and "initializer" functions
    #     .reduce(reducer=update_candle, initializer=init_candle)
    # )

    # starts the streaming app
    app.run()


if __name__ == '__main__':
    run(
        kafka_broker_address='localhost:31234',
        kafka_input_topic='trades',
        kafka_output_topic='candles',
        kafka_consumer_group='candles_consumer_group',
        candle_sec=60,
    )
