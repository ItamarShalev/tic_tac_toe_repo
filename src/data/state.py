from __future__ import annotations
from enum import Enum


class State(Enum):
    X_WIN = "X"
    O_WIN = "O"
    DRAW = "DRAW"
    X_TURN = "X_TURN"
    O_TURN = "O_TURN"

    @classmethod
    def from_str(cls, value: str | State):
        if not value:
            raise ValueError(f"Got invalid value: {value}")
        if isinstance(value, State):
            return value
        try:
            return cls[value.replace(" ", "_").upper()]
        except KeyError:
            raise ValueError(f"Invalid State name: {value}") from None

    def game_over(self) -> bool:
        return self in (State.X_WIN, State.O_WIN, State.DRAW)

    def __repr__(self):
        return f"State(name: {self.name}, value: {self.value})"

    def __str__(self):
        return self.name
