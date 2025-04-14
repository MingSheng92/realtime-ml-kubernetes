# perform stateful transformation with quixstream
from loguru import logger
from quixstreams import Application


def init_candle(trade: dict) -> dict:
    """
    Initialize a candle with the first trade
    Returns the initial candle state

    Args:
        trade (dict): The first trade

    Returns:
        dict: The initial candle state
    """
    return {
        'open': trade['price'],
        'high': trade['price'],
        'low': trade['price'],
        'close': trade['price'],
        'volume': trade['quantity'],
        'pair': trade['product_id'],
    }


def update_candle(candle: dict, trade: dict) -> dict:
    """
    Takes the current candle (aka state) and the new trade, and updates the candle state

    Args:
        candle (dict): The current candle state
        trade (dict): The new trade

    Returns:
        dict: The updated candle state
    """
    # open price does not change, so there is no need to update it
    candle['high'] = max(candle['high'], trade['price'])
    candle['low'] = min(candle['low'], trade['price'])
    candle['close'] = trade['price']
    candle['volume'] += trade['quantity']

    return candle


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
    # sdf = sdf.update(lambda message: logger.info(f'Input: {message}'))
    from datetime import timedelta

    # aggregate trades into candles using tumbling windows
    sdf = (
        # degine tumbling windows of 10 minutes
        sdf.tumbling_window(timedelta(seconds=candle_sec))
        # create a reduce aggregation with a "reducer" and "initializer" functions
        .reduce(reducer=update_candle, initializer=init_candle)
    )

    # we emit all intermediate candles to make the system more responsive
    sdf = sdf.current()

    # Extract open, high, low, close, volume, timestamp_ms, pair from the dataframe
    sdf['open'] = sdf['value']['open']
    sdf['high'] = sdf['value']['high']
    sdf['low'] = sdf['value']['low']
    sdf['close'] = sdf['value']['close']
    sdf['volume'] = sdf['value']['volume']
    sdf['pair'] = sdf['value']['pair']

    # Extract window start and end timestamps
    sdf['window_start_ms'] = sdf['start']
    sdf['window_end_ms'] = sdf['end']

    # keep only the relevant columns
    sdf = sdf[
        [
            'pair',
            'open',
            'high',
            'low',
            'close',
            'volume',
            'window_start_ms',
            'window_end_ms',
        ]
    ]

    sdf['candle_seconds'] = candle_sec

    # logging on the console
    sdf = sdf.update(lambda value: logger.debug(f'Candle: {value}'))

    # Step 3. Produce the candles to the output kafka topic
    sdf = sdf.to_topic(candles_topic)

    # Starts the streaming app
    app.run()


if __name__ == '__main__':
    run(
        kafka_broker_address='localhost:31234',
        kafka_input_topic='trades',
        kafka_output_topic='candles',
        kafka_consumer_group='candles_consumer_group',
        candle_sec=60,
    )
