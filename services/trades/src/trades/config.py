from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # load from our env file
    model_config = SettingsConfigDict(
        env_file='services/trades/settings.env', env_file_encoding='utf-8'
    )

    product_ids: list[str] = [
        'BTC/USD',
        'BTC/EUR',
        'ETH/USD',
        'ETH/EUR',
        'SOL/USD',
        'SOL/EUR',
        'XRP/USD',
        'XRP/EUR',
    ]
    kafka_broker_address: str
    kafka_topic_name: str


config = Settings()
# print(settings.model_dump())
