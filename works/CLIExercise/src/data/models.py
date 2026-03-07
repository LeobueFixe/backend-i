#Imports

from dataclasses import dataclass

#Dataclass For currency
@dataclass
class Currency:
    code: str
    name: str
    symbol: str = ""
