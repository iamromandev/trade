import re

_SORT_REGEX = re.compile(r"^-?[a-zA-Z_][a-zA-Z0-9_]*$")


def parse_sort_string(sort: str) -> list[str]:
    return [part.strip() for part in sort.split(",") if part.strip()]


def resolve_order_by(sort_parts: list[str], allowed_fields: set[str], default: list[str] | None = None) -> list[str]:
    result = []
    for part in sort_parts:
        if not _SORT_REGEX.match(part):
            return default or ["-created_at"]
        field = part.lstrip("-")
        if field not in allowed_fields:
            return default or ["-created_at"]
        result.append(part)
    return result or default or ["-created_at"]
