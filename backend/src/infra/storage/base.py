import mimetypes
import re

_KEY_REGEX = re.compile(r"^[a-zA-Z0-9_./-]{1,512}$")


class BaseFileStorage:
    def _validate_key(self, key: str) -> None:
        if not _KEY_REGEX.match(key):
            raise ValueError(f"Invalid storage key: {key}")

    def _infer_content_type(self, key: str) -> str:
        ct, _ = mimetypes.guess_type(key)
        return ct or "application/octet-stream"

    def _normalise_path(self, key: str) -> str:
        return key.lstrip("/")
