from dataclasses import dataclass

@dataclass
class Currency:
    code: str
    name: str
    symbol: str = ""
