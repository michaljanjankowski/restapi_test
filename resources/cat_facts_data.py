from dataclasses import dataclass


@dataclass
class Fact:
    fact: str
    length: int

    @classmethod
    def from_dict(cls, data: dict) -> "Fact":
        assert isinstance(data, dict), "Expected a fact object"
        assert isinstance(data.get("fact"), str), "Expected fact text"
        assert isinstance(data.get("length"), int), "Expected fact length"
        return cls(fact=data["fact"], length=data["length"])
