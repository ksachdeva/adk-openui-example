from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from fastapi import FastAPI

from backend._constants import API_PREFIX_SIMPLE_AGENT
from backend.agents import SimpleAgent


def register_simple_agent(
    simple_agent: SimpleAgent,
    app: FastAPI,
) -> None:

    simple_ag_ui_agent = ADKAgent(
        adk_agent=simple_agent,
        app_name="demo_app",
        user_id="demo_user",
        session_timeout_seconds=3600,
        use_in_memory_services=True,
    )

    add_adk_fastapi_endpoint(app, simple_ag_ui_agent, path=API_PREFIX_SIMPLE_AGENT)
