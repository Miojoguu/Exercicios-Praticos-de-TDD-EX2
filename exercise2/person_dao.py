"""Person repository and validation entry point."""

from exercise2.models import Person


class PersonDAO:
    """Store valid people and report validation errors."""

    INVALID_NAME = (
        "O nome deve conter pelo menos duas partes compostas apenas por letras."
    )
    INVALID_AGE = "A idade deve estar entre 1 e 200."
    EMAIL_REQUIRED = "A pessoa deve ter pelo menos um e-mail."
    INVALID_EMAIL = "O e-mail '{value}' possui formato inválido."

    def __init__(self) -> None:
        self._people: list[Person] = []

    @property
    def people(self) -> tuple[Person, ...]:
        """Return an immutable view of the saved people."""

        return tuple(self._people)

    def save(self, person: Person) -> None:
        """Save a valid person."""

        raise NotImplementedError

    def isValidToInclude(self, person: Person) -> list[str]:  # noqa: N802
        """Return every validation error found for ``person``."""

        raise NotImplementedError

