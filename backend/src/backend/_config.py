import enum
import os
from typing import Annotated, Any

from pydantic import AnyUrl, BeforeValidator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .agents import AgentConfig


class DeploymentMode(str, enum.Enum):
    dev = "dev"
    staging = "staging"
    prod = "prod"


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class BackendConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.getenv("MASTER_ENV_FILE", ".env"),
        env_prefix="BACKEND_",
        env_ignore_empty=True,
        extra="ignore",
    )

    simple_agent: AgentConfig

    frontend_host: str = "http://localhost:5173"

    PROJECT_NAME: str = "Backend Template"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        origins = [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS]
        origins = origins + [self.frontend_host]

        if self.DEPLOYMENT_MODE != DeploymentMode.prod:
            origins.append("http://127.0.0.1:5173")
            origins.append("http://localhost:5173")
            origins.append("http://localhost:5174")
            origins.append("http://localhost:3000")
            origins.append("http://localhost:50489")
            origins.append("http://0.0.0.0:5173")
            origins.append("http://0.0.0.0:3000")

        return origins

    DEPLOYMENT_MODE: DeploymentMode = DeploymentMode.dev
