from dataclasses import dataclass, asdict
from datetime import date


@dataclass(frozen=True)
class City:
    name: str
    country: str
    population_evolution: tuple[tuple[date, int], ...]

    def to_json(self) -> dict:
        return asdict(self)

