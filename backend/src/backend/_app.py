from contextlib import asynccontextmanager
from typing import AsyncGenerator

import fastapi
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from ._config import BackendConfig, DeploymentMode
from .api import (
    dummy_router,
    health_router,
)


@asynccontextmanager
async def internal_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        yield
    finally:
        await app.state.dishka_container.close()


class App(fastapi.FastAPI):
    def __init__(self, config: BackendConfig) -> None:
        super().__init__(
            title=config.PROJECT_NAME,
            docs_url="/docs"
            if config.DEPLOYMENT_MODE in [DeploymentMode.dev, DeploymentMode.staging]
            else None,
            redoc_url=None,
            lifespan=internal_lifespan,
        )

        if config.all_cors_origins:
            self.add_middleware(
                CORSMiddleware,
                allow_origins=config.all_cors_origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        self.include_router(health_router)
        self.include_router(dummy_router)
