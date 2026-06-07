import "@openuidev/react-ui/components.css";
import "@openuidev/react-ui/styles/index.css";

import { FullScreen } from "@openuidev/react-ui";
import { openuiChatLibrary } from "@openuidev/react-ui/genui-lib";

// The apiUrl example (see commented) does not work
// because it is missing essential information such as runId, state, context, tools, and forwardedProps.
//
// Fortunately, the processMessage example demonstrates how to include all necessary information in the request body,
// ensuring that the backend can process the messages correctly and maintain the conversation state across interactions.

export default function App() {
  return (
    <div className="h-screen w-screen overflow-hidden">
      {/* <FullScreen
        apiUrl="/api/v1/agents/simple-agent"
        componentLibrary={openuiChatLibrary}
        conversationStarters={{
          variant: "short",
          options: [
            {
              displayText: "Weather in Tokyo",
              prompt: "What's the weather like in Tokyo right now?",
            },
            { displayText: "AAPL stock price", prompt: "What's the current Apple stock price?" },
            {
              displayText: "Contact form",
              prompt: "Build me a contact form with name, email, topic, and message fields.",
            },
            {
              displayText: "Data table",
              prompt:
                "Show me a table of the top 5 programming languages by popularity with year created.",
            },
          ],
        }}
      /> */}

      <FullScreen
        processMessage={async ({ threadId, messages, abortController }) => {

          const runId = crypto.randomUUID();
          console.log("Generated runId:", runId);

          return fetch("/api/v1/agents/simple-agent", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              threadId,
              state: {},
              context: [],
              tools:[],
              forwardedProps:{},
              runId: runId,
              messages: messages,
            }),
            signal: abortController.signal,
          });
        }}
        componentLibrary={openuiChatLibrary}
        conversationStarters={{
          variant: "short",
          options: [
            {
              displayText: "Weather in Tokyo",
              prompt: "What's the weather like in Tokyo right now?",
            },
            { displayText: "AAPL stock price", prompt: "What's the current Apple stock price?" },
            {
              displayText: "Contact form",
              prompt: "Build me a contact form with name, email, topic, and message fields.",
            },
            {
              displayText: "Data table",
              prompt:
                "Show me a table of the top 5 programming languages by popularity with year created.",
            },
          ],
        }}
      />
    </div>
  );
}
