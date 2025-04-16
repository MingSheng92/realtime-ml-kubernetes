from loguru import logger
from quixstreams import Application


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
    candles_topic = app.topic(kafka_input_topic, value_deserializer='json')
    # output topic
    techinical_indicators_topic = app.topic(kafka_output_topic, value_serializer='json')

    # step 1: ingest candles from topic,
    # input kafka topic
    sdf = app.dataframe(topic=candles_topic)

    # Filter the candles for the given 'candles_seconds'
    sdf = sdf[sdf['candle_seconds'] == candle_sec]

    # step 2: Compute technical indicators from candles
    # TODO : data processing here

    # logging on the console
    sdf = sdf.update(lambda value: logger.debug(f'Final message: {value}'))

    # Step 3. Produce the candles to the output kafka topic
    sdf = sdf.to_topic(techinical_indicators_topic)

    # Starts the streaming app
    app.run()


if __name__ == '__main__':
    from technical_indicators.config import config

    run(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        candle_sec=config.candle_sec,
    )
