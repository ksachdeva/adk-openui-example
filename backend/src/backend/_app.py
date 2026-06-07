from contextlib import asynccontextmanager
from typing import AsyncGenerator

import fastapi
from fastapi import FastAPI
from google.adk.models.lite_llm import LiteLlm
from starlette.middleware.cors import CORSMiddleware

from ._config import BackendConfig, DeploymentMode
from .agents import SimpleAgent
from .api import (
    dummy_router,
    health_router,
    register_simple_agent,
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

        # create the SimpleAgent and then register it with the app
        simple_agent = SimpleAgent(
            llm=LiteLlm(
                model=config.simple_agent.llm.model_name,
                **config.simple_agent.llm.provider_args,
            ),
            generate_content_config=config.simple_agent.generate_content,
        )

        register_simple_agent(simple_agent, self)
