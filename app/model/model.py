from dataclasses import dataclass


@dataclass
class Loc:
    px: int = 1
    py: int = 1

    def __str__(self) -> str:
        return f"({self.px}, {self.py})"
