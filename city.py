from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class City:
    name: str
    country: str
    population: int

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, json: dict) -> City:
        return City(
            name=json["name"],
            country=json["country"],
            population=json["population"],
        )
