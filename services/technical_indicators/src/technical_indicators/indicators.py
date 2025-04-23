from loguru import logger
from talib import stream


def compute_technical_indicators(
    candle: dict,
    state: dict,
):
    """
    Computes technical indicators from the candles in the state dictionary.

    Args:
        candles (list): List of candles in the state dictionary

    Returns:
        dict: Dictionary with the computed technical indicators
    """
    import numpy as np

    # Extract the candles from the state dictionary
    candles = state.get('candles', default=[])

    logger.debug(f'Number of candles in state: {len(candles)}')

    # Extract the open, close, high, low, volume candles (which is a list of dictionaries)
    # into numpy arrays, because this is the type that TA-Lib expects to compute the indicators
    _open = np.array([c['open'] for c in candles])
    _high = np.array([c['high'] for c in candles])
    _low = np.array([c['low'] for c in candles])
    close = np.array([c['close'] for c in candles])
    _volume = np.array([c['volume'] for c in candles])

    indicators = {}

    # Simple Moving Average (SMA) for different periods
    # indicators['sma_1'] = stream.SMA(close, timeperiod=1) # just to check the type
    indicators['sma_7'] = stream.SMA(close, timeperiod=7)
    indicators['sma_14'] = stream.SMA(close, timeperiod=14)
    indicators['sma_21'] = stream.SMA(close, timeperiod=21)
    indicators['sma_60'] = stream.SMA(close, timeperiod=60)

    # breakpoint()

    return {
        **candle,
        **indicators,
    }
