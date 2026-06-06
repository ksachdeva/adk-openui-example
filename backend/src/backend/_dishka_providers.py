from typing import Sequence

from dishka import Provider, Scope

from ._config import BackendConfig


def get_providers() -> Sequence[Provider]:
    runner_provider = Provider(scope=Scope.APP)
    runner_provider.from_context(BackendConfig)

    return [runner_provider]
