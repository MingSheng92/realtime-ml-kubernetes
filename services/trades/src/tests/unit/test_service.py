import json
import time
from unittest.mock import Mock, call, patch

import pytest
from trades.main import run


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

    @patch('trades.main.Application')
    def test_run_produces_messages_to_kafka(self, MockApplication, mock_kraken_api):
        """Test that the run method produces messages to Kafka"""
        # Mock the Kafka producer
        mock_app = MockApplication.return_value
        mock_topic = Mock()
        mock_topic.name = 'test_topic'
        mock_app.topic.return_value = mock_topic

        mock_producer = Mock()
        mock_app.get_producer.return_value.__enter__.return_value = mock_producer

        # mock serialized messages
        mock_message1 = Mock()
        mock_message1.key = 'BTC-USD'
        mock_message1.value = json.dump(
            mock_kraken_api.get_trades.return_value[0].to_dict.return_value
        )

        mock_message2 = Mock()
        mock_message2.key = 'ETH-USD'
        mock_message2.value = json.dump(
            mock_kraken_api.get_trades.return_value[1].to_dict.return_value
        )

        mock_topic.serialize.side_effect = [mock_message1, mock_message2]

        # call the function with max_iterations=1 to run just one cycle
        run(
            kafka_broker_address='localhost:31234',
            kafka_topic_name='test_topic',
            kraken_api=mock_kraken_api,
            max_iterations=1,
        )

        # Assertions
        MockApplication.assert_called_once_with(
            kafka_broker_address='localhost:31234',
        )
        mock_app.topic.assert_called_once_with(
            name='test_topic', value_serializer='json'
        )
        assert mock_kraken_api.get_trades.call_count == 1

        # check serialized calls
        assert mock_topic.serialize.call_count == 2
        mock_topic.serialize.assert_has_calls(
            [
                call(
                    key='BTC-USD',
                    value=mock_kraken_api.get_trades.return_value[
                        0
                    ].to_dict.return_value,
                ),
                call(
                    key='ETH-USD',
                    value=mock_kraken_api.get_trades.return_value[
                        1
                    ].to_dict.return_value,
                ),
            ]
        )

        # check produce calls
        assert mock_producer.produce.call_count == 2
        mock_producer.produce.assert_has_calls(
            [
                call(
                    topic=mock_topic, key=mock_message1.key, value=mock_message1.value
                ),
                call(
                    topic=mock_topic, key=mock_message2.key, value=mock_message2.value
                ),
            ]
        )
