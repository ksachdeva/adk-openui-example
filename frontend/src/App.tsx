import "@openuidev/react-ui/components.css";
import "@openuidev/react-ui/styles/index.css";

import { FullScreen } from "@openuidev/react-ui";
import { openuiChatLibrary } from "@openuidev/react-ui/genui-lib";

export default function App() {
  return (
    <div className="h-screen w-screen overflow-hidden">
      <FullScreen
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
      />
    </div>
  );
}
