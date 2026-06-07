from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.genai import types as genai_types

_INSTRUCTION = """
    You are a helpful assistant. Help users by answering their questions and assisting with their needs.
    - If the user greets you, please greet them back with specifically with "Hello".
    - If the user greets you and does not make any request, greet them and ask "how can I assist you?"
    - If the user makes a statement without making a request, you do not need to tell them you can't do anything about it.
      Try to say something conversational about it in response, making sure to mention the topic directly.
    - If the user asks you a question, if possible you can answer it using previous context without telling them that you cannot look it up.
      Only tell the user that you cannot search if you do not have enough information already to answer.
    """.strip()


class SimpleAgent(LlmAgent):
    def __init__(
        self,
        llm: LiteLlm,
        generate_content_config: genai_types.GenerateContentConfig | None = None,
    ) -> None:
        self._llm = llm

        static_instruction_path = Path(__file__).parent / "system-prompt.txt"

        static_instruction = (
            static_instruction_path.read_text()
            if static_instruction_path.exists()
            else ""
        )

        super().__init__(
            name="simple_agent",
            description="You are a helpful assistant. Help users by answering their questions and assisting with their needs.",
            model=self._llm,
            instruction=_INSTRUCTION,
            static_instruction=static_instruction,
            tools=[],
            generate_content_config=generate_content_config,
        )
