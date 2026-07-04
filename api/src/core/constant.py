from tortoise.exceptions import DoesNotExist, IntegrityError

from src.core.type import Code, ErrorType

EXCEPTION_TO_CODE: dict[type, tuple[Code, ErrorType]] = {
    ValueError: (Code.BAD_REQUEST, ErrorType.VALIDATION_ERROR),
    KeyError: (Code.BAD_REQUEST, ErrorType.VALIDATION_ERROR),
    DoesNotExist: (Code.NOT_FOUND, ErrorType.NOT_FOUND),
    IntegrityError: (Code.CONFLICT, ErrorType.DB_INTEGRITY_ERROR),
}
