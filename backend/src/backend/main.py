from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from backend._config import BackendConfig
from backend._dishka_providers import get_providers

from ._app import App

config = BackendConfig()


def create_app(config: BackendConfig) -> App:
    app = App(config=config)
    setup_dishka(container, app)
    return app


# Make the container with settings in context
container = make_async_container(
    *get_providers(),
    context={
        BackendConfig: config,
    },
)

# Make the app
app = create_app(config=config)
