from ._dummy import router as dummy_router
from ._health import router as health_router
from ._simple_agent import register_simple_agent

__all__ = [
    "dummy_router",
    "health_router",
    "register_simple_agent",
]
