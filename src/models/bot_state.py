from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class BotState:
    id: str
    name: str
    pair: str
    strategy: str
    exchange: str
    status: str
    
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
        