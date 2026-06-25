from dataclasses import dataclass


@dataclass
class AIResponse:
    content: str
    provider: str
    metadata: dict


class BaseAIProvider:
    provider_name = "base"

    def complete(self, messages, temperature=0.3):
        raise NotImplementedError

