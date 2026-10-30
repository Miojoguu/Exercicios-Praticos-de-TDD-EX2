"""Domain models represented in the exercise class diagram."""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Email:
    """An e-mail address associated with a person."""

    id: int
    name: str


@dataclass(slots=True)
class Person:
    """A person and their associated e-mail addresses."""

    id: int
    name: str
    age: int
    emails: list[Email] = field(default_factory=list)

