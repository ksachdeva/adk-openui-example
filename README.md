# Google ADK with OpenUI Frontend

> This is a devcontainer based repository so simply open it in vscode & re-open in devcontainer. Everything will be set for you!

This example demonstrates how to build a conversational AI application using Google ADK (Agent Development Kit) as the backend agent framework, exposed via the ag-ui protocol, and consumed by an OpenUI-based frontend.

## Architecture Overview

This project integrates three key technologies:

1. **Google ADK** - Agent framework for building conversational AI agents
2. **ag-ui-adk** - Translation layer that converts Google ADK events/messages to ag-ui protocol and vice-versa
3. **OpenUI** - React-based UI library with native ag-ui protocol support

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                        │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │          OpenUI React Components                          │  │
│  │         (@openuidev/react-ui)                             │  │
│  │                                                           │  │
│  │  • FullScreen chat interface                              │  │
│  │  • processMessage callback                                │  │
│  │  • Conversation starters                                  │  │
│  └─────────────────────┬─────────────────────────────────────┘  │
│                        │                                        │
└────────────────────────┼───────────────────────────────────────┘
                         │
                         │ ag-ui Protocol (JSON/SSE)
                         │ RunAgentInput payload:
                         │ {threadId, runId, messages, state,
                         │  context, tools, forwardedProps}
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                          │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │           ag-ui-adk Translation Layer                     │  │
│  │                                                           │  │
│  │  ADKAgent wrapper:                                        │  │
│  │  • Converts ag-ui messages → ADK events                   │  │
│  │  • Converts ADK events → ag-ui messages                   │  │
│  │  • Manages session state & context                        │  │
│  └─────────────────────┬─────────────────────────────────────┘  │
│                        │                                        │
│                        ▼                                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │           Google ADK Agent                                │  │
│  │                                                           │  │
│  │  • Agent logic & system prompts                           │  │
│  │  • LLM integration (Gemini, etc.)                         │  │
│  │  • Tool/function calling                                  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## How It Works

### Backend Implementation

The backend uses Google ADK to define the agent logic and exposes it via ag-ui protocol:

1. **Google ADK Agent** (`backend/agents/_simple_agent.py`) - Defines the agent behavior, system prompts, and capabilities
2. **ag-ui-adk Wrapper** (`backend/api/_simple_agent.py`) - Wraps the ADK agent with `ADKAgent` class and uses `add_adk_fastapi_endpoint()` to expose it as a FastAPI endpoint
3. **FastAPI Server** - Serves the ag-ui compatible endpoint at `/api/v1/agents/simple-agent`

```python
# Backend wrapping code
simple_ag_ui_agent = ADKAgent(
    adk_agent=simple_agent,
    app_name="demo_app",
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True,
)

add_adk_fastapi_endpoint(app, simple_ag_ui_agent, path=API_PREFIX_SIMPLE_AGENT)
```

The `ag-ui-adk` library handles the protocol translation bidirectionally:
- **Incoming**: ag-ui `RunAgentInput` → ADK events
- **Outgoing**: ADK agent responses → ag-ui formatted messages (text, UI components, etc.)

### Frontend Implementation

The frontend uses OpenUI's React components with native ag-ui protocol support:

```typescript
<FullScreen
  processMessage={async ({ threadId, messages, abortController }) => {
    const runId = crypto.randomUUID();
    return fetch("/api/v1/agents/simple-agent", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        threadId, runId, messages,
        state: {}, context: [], tools: [], forwardedProps: {}
      }),
      signal: abortController.signal,
    });
  }}
  componentLibrary={openuiChatLibrary}
/>
```

### Known Issue & Workaround

**Bug in OpenUI's Native Implementation**: The OpenUI library's `apiUrl` prop does not send a correct `RunAgentInput` payload. It omits essential fields required by the ag-ui protocol:
- `runId` - Unique identifier for each agent run
- `state` - Agent state for maintaining context
- `context` - Additional context data
- `tools` - Available tools/functions
- `forwardedProps`

**Workaround**: Use the `processMessage` callback instead of `apiUrl` to manually construct the complete payload. See [`frontend/src/App.tsx`](frontend/src/App.tsx) for the implementation. The commented-out `apiUrl` example shows the approach that doesn't work.

## Getting Started

### Running the Application

1. **Start the backend**:

```bash
# issue this from the root of the repo
poe dev-run-backend
```

This starts the FastAPI server with the ADK agent exposed via ag-ui protocol.

2. **Start the frontend**:

```bash
# needed only one time
cd frontend
npm install
```

```bash
# issue this from the root of the repo
poe dev-run-frontend
```

This starts the Vite development server with the OpenUI React application.

3. Open your browser to the frontend URL (typically `http://localhost:5173`)

## Project Structure

```
├── backend/              # FastAPI backend with Google ADK
│   └── src/backend/
│       ├── agents/       # ADK agent definitions
│       └── api/          # ag-ui-adk endpoint registration
├── frontend/             # OpenUI React frontend
│   └── src/
│       └── App.tsx       # Main app with ag-ui integration
└── poe.toml             # Task definitions for running services
```

## Learn More

- [Google ADK](https://github.com/google/adk-python) - Agent Development Kit
- [ag-ui Protocol](https://github.com/ag-ui-protocol/ag-ui) - Agent UI communication protocol
- [OpenUI](https://github.com/thesysdev/openui) - React Generative UI library for conversational AI
