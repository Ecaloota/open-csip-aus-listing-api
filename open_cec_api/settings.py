from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings for the Open CEC API.
    """

    schema_version: Literal["v1", "v2"] = "v1"
    host: str = "0.0.0.0"  # listen on all interfaces
    port: int = 8080
    workers_count: int = 1
    reload: bool = False

    api_key_hash: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="OPEN_CEC_API_",
        extra="allow",  # allow extra fields in the settings
    )


settings = Settings()  # type: ignore[call-arg]  # instantiated at runtime
