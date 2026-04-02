from datetime import datetime
from core.errors import ValidationError


def _validate_nonempty_string(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field_name} is required")


def validate_title(value: str) -> None:
    _validate_nonempty_string(value, "Title")
    if len(value.strip()) > 100:
        raise ValidationError("Title must be 100 characters or fewer")


def validate_owner(value: str) -> None:
    _validate_nonempty_string(value, "Owner")
    if len(value.strip()) > 100:
        raise ValidationError("Owner must be 100 characters or fewer")


def validate_iso_date(value: str) -> None:
    _validate_nonempty_string(value, "Date")
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValidationError("Date must be YYYY-MM-DD") from exc