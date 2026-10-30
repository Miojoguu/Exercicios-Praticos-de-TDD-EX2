"""Behavior specified first for the PersonDAO TDD cycle."""

import pytest

from exercise2 import Email, Person, PersonDAO


def make_person(
    *,
    name: str = "Maria da Silva",
    age: int = 35,
    emails: list[Email] | None = None,
) -> Person:
    if emails is None:
        emails = [Email(id=1, name="maria.silva@example.com")]
    return Person(id=1, name=name, age=age, emails=emails)


class TestIsValidToInclude:
    def test_returns_no_errors_for_a_valid_person(self) -> None:
        errors = PersonDAO().isValidToInclude(make_person())

        assert errors == []

    @pytest.mark.parametrize("age", [1, 200])
    def test_accepts_age_boundary_values(self, age: int) -> None:
        errors = PersonDAO().isValidToInclude(make_person(age=age))

        assert PersonDAO.INVALID_AGE not in errors

    @pytest.mark.parametrize("age", [0, 201, -1, None, True])
    def test_rejects_age_outside_the_closed_interval(self, age: object) -> None:
        person = make_person()
        person.age = age  # type: ignore[assignment]

        errors = PersonDAO().isValidToInclude(person)

        assert errors == [PersonDAO.INVALID_AGE]

    @pytest.mark.parametrize(
        "name",
        [
            "Maria",
            "Maria Silva3",
            "Maria-Silva Costa",
            "",
            "   ",
            None,
        ],
    )
    def test_rejects_name_without_two_alphabetic_parts(self, name: object) -> None:
        person = make_person()
        person.name = name  # type: ignore[assignment]

        errors = PersonDAO().isValidToInclude(person)

        assert errors == [PersonDAO.INVALID_NAME]

    @pytest.mark.parametrize(
        "name",
        ["João Ávila", "Ana Maria", "  Maria   da Silva  "],
    )
    def test_accepts_unicode_letters_and_ignores_extra_spaces(self, name: str) -> None:
        errors = PersonDAO().isValidToInclude(make_person(name=name))

        assert PersonDAO.INVALID_NAME not in errors

    def test_requires_at_least_one_email(self) -> None:
        errors = PersonDAO().isValidToInclude(make_person(emails=[]))

        assert errors == [PersonDAO.EMAIL_REQUIRED]

    def test_treats_none_email_collection_as_missing(self) -> None:
        person = make_person()
        person.emails = None  # type: ignore[assignment]

        errors = PersonDAO().isValidToInclude(person)

        assert errors == [PersonDAO.EMAIL_REQUIRED]

    @pytest.mark.parametrize(
        "address",
        [
            "ana@example.com",
            "ana.silva@subdomain.com.br",
            "a@b.c",
        ],
    )
    def test_accepts_email_with_nonempty_local_domain_and_suffix(
        self, address: str
    ) -> None:
        person = make_person(emails=[Email(id=1, name=address)])

        errors = PersonDAO().isValidToInclude(person)

        assert errors == []

    @pytest.mark.parametrize(
        "address",
        [
            "anaexample.com",
            "@example.com",
            "ana@.com",
            "ana@example.",
            "ana@example..com",
            "ana @example.com",
            "ana@example .com",
            "ana@@example.com",
        ],
    )
    def test_rejects_malformed_email(self, address: str) -> None:
        errors = PersonDAO().isValidToInclude(
            make_person(emails=[Email(id=1, name=address)])
        )

        assert errors == [PersonDAO.INVALID_EMAIL.format(value=address)]

    def test_reports_each_invalid_email_in_association_order(self) -> None:
        person = make_person(
            emails=[
                Email(id=1, name="first-invalid"),
                Email(id=2, name="valid@example.com"),
                Email(id=3, name="second-invalid"),
            ]
        )

        errors = PersonDAO().isValidToInclude(person)

        assert errors == [
            PersonDAO.INVALID_EMAIL.format(value="first-invalid"),
            PersonDAO.INVALID_EMAIL.format(value="second-invalid"),
        ]

    def test_rejects_email_object_without_a_textual_name(self) -> None:
        person = make_person()
        person.emails = [None, Email(id=2, name=None)]  # type: ignore[list-item,arg-type]

        errors = PersonDAO().isValidToInclude(person)

        assert errors == [
            PersonDAO.INVALID_EMAIL.format(value=None),
            PersonDAO.INVALID_EMAIL.format(value=None),
        ]

    def test_accumulates_errors_in_rule_order(self) -> None:
        person = make_person(name="Maria", age=0, emails=[])

        errors = PersonDAO().isValidToInclude(person)

        assert errors == [
            PersonDAO.INVALID_NAME,
            PersonDAO.INVALID_AGE,
            PersonDAO.EMAIL_REQUIRED,
        ]


class TestSave:
    def test_saves_a_valid_person(self) -> None:
        dao = PersonDAO()
        person = make_person()

        result = dao.save(person)

        assert result is None
        assert dao.people == (person,)

    def test_does_not_save_an_invalid_person(self) -> None:
        dao = PersonDAO()

        with pytest.raises(ValueError, match=PersonDAO.INVALID_NAME):
            dao.save(make_person(name="Maria"))

        assert dao.people == ()

