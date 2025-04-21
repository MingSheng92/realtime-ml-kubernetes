import time
from unittest.mock import Mock

import pytest


class TestTradeService:
    @pytest.fixture
    def mock_kraken_api(self):
        """create mock api"""
        mock_api = Mock()

        trade1 = Mock()
        trade1.to_dict.return_value = {
            'product_id': 'BTC-USD',
            'price': 10000.00,
            'quantity': 0.001,
            'timestamp': time.time(),
        }

        trade2 = Mock()
        trade2.to_dict.return_value = {
            'product_id': 'ETH-USD',
            'price': 3000.00,
            'quantity': 0.01,
            'timestamp': time.time(),
        }

        mock_api.get_trades.return_value = [trade1, trade2]
        return mock_api
