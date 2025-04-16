from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # load from our env file
    model_config = SettingsConfigDict(
        env_file='services/technical_indicators/settings.env', env_file_encoding='utf-8'
    )

    kafka_broker_address: str
    kafka_input_topic: str
    kafka_output_topic: str
    kafka_consumer_group: str
    candle_sec: int


config = Settings()
# print(settings.model_dump())
