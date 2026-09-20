from dataclasses import asdict, dataclass
from typing import List, Optional


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


@dataclass
class FactsQuery:
    limit: Optional[int] = None
    max_length: Optional[int] = None
    page: Optional[int] = None

    def to_params(self) -> dict:
        return {key: value for key, value in asdict(self).items() if value is not None}


@dataclass
class BreedsQuery:
    limit: int

    def to_params(self) -> dict:
        return asdict(self)


@dataclass
class FactsPage:
    current_page: int
    data: List[Fact]

    @classmethod
    def from_dict(cls, data: dict) -> "FactsPage":
        return cls(
            current_page=data["current_page"],
            data=[Fact.from_dict(item) for item in data["data"]],
        )


@dataclass
class Breed:
    breed: str
    country: str
    origin: str
    coat: str
    pattern: str

    @classmethod
    def from_dict(cls, data: dict) -> "Breed":
        return cls(**{field: data[field] for field in cls.__dataclass_fields__})


@dataclass
class BreedsPage:
    data: List[Breed]

    @classmethod
    def from_dict(cls, data: dict) -> "BreedsPage":
        return cls(data=[Breed.from_dict(item) for item in data["data"]])


@dataclass
class ApiError:
    message: str

    @classmethod
    def from_dict(cls, data: dict) -> "ApiError":
        return cls(message=data["message"])
