from dataclasses import dataclass


@dataclass
class SetMenuDTO:
    name: str
    vegan: bool
    vegetarian: bool
    glutenfree: bool
    price_us: float
