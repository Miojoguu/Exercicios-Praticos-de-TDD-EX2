"""Person repository and validation entry point."""

import re

from exercise2.models import Person


class PersonDAO:
    """Store valid people and report validation errors."""

    INVALID_NAME = (
        "O nome deve conter pelo menos duas partes compostas apenas por letras."
    )
    INVALID_AGE = "A idade deve estar entre 1 e 200."
    EMAIL_REQUIRED = "A pessoa deve ter pelo menos um e-mail."
    INVALID_EMAIL = "O e-mail '{value}' possui formato inválido."
    _EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+$")

    def __init__(self) -> None:
        self._people: list[Person] = []

    @property
    def people(self) -> tuple[Person, ...]:
        """Return an immutable view of the saved people."""

        return tuple(self._people)

    def save(self, person: Person) -> None:
        """Save a valid person."""

        errors = self.isValidToInclude(person)
        if errors:
            raise ValueError(" ".join(errors))
        self._people.append(person)

    def isValidToInclude(self, person: Person) -> list[str]:  # noqa: N802
        """Return every validation error found for ``person``."""

        errors: list[str] = []

        name = getattr(person, "name", None)
        name_parts = name.split() if isinstance(name, str) else []
        if len(name_parts) < 2 or not all(part.isalpha() for part in name_parts):
            errors.append(self.INVALID_NAME)

        age = getattr(person, "age", None)
        if (
            not isinstance(age, int)
            or isinstance(age, bool)
            or not 1 <= age <= 200
        ):
            errors.append(self.INVALID_AGE)

        emails = getattr(person, "emails", None)
        if not emails:
            errors.append(self.EMAIL_REQUIRED)
        else:
            for email in emails:
                value = getattr(email, "name", None)
                if not isinstance(value, str) or not self._EMAIL_PATTERN.fullmatch(value):
                    errors.append(self.INVALID_EMAIL.format(value=value))

        return errors

