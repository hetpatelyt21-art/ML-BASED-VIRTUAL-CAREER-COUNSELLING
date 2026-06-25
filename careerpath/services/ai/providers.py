import os

from .base import AIResponse, BaseAIProvider


class OpenAIProvider(BaseAIProvider):
    provider_name = "openai"

    def complete(self, messages, temperature=0.3):
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install the openai package to use OpenAIProvider.") from exc
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=messages,
            temperature=temperature,
        )
        return AIResponse(
            content=response.choices[0].message.content or "",
            provider=self.provider_name,
            metadata={"model": response.model},
        )


class ClaudeProvider(BaseAIProvider):
    provider_name = "claude"

    def complete(self, messages, temperature=0.3):
        try:
            import anthropic
        except ImportError as exc:
            raise RuntimeError("Install the anthropic package to use ClaudeProvider.") from exc
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        system = messages[0]["content"] if messages and messages[0]["role"] == "system" else ""
        user_messages = [message for message in messages if message["role"] != "system"]
        response = client.messages.create(
            model=os.environ.get("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest"),
            system=system,
            messages=user_messages,
            temperature=temperature,
            max_tokens=900,
        )
        content = "\n".join(block.text for block in response.content if getattr(block, "type", "") == "text")
        return AIResponse(content=content, provider=self.provider_name, metadata={"model": response.model})


def get_ai_provider(name=None):
    provider = (name or os.environ.get("AI_PROVIDER", "openai")).lower()
    if provider == "claude":
        return ClaudeProvider()
    return OpenAIProvider()

