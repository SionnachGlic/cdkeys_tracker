""""Contains the Game dataclass"""

from dataclasses import dataclass

@dataclass
class Game:
    """A class representing a game with its attributes."""
    url: str
    title: str
    current_price: float
    max_price: float