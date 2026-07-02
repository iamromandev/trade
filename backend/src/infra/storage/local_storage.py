from pathlib import Path

from src.infra.storage.base import BaseFileStorage


class LocalFileStorage(BaseFileStorage):
    def __init__(self, base_path: str = "./storage"):
        self._base = Path(base_path).resolve()
        self._base.mkdir(parents=True, exist_ok=True)

    async def put(self, key: str, content: bytes) -> str:
        self._validate_key(key)
        path = self._resolve(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return str(path)

    async def get(self, key: str) -> bytes | None:
        self._validate_key(key)
        path = self._resolve(key)
        if path.exists():
            return path.read_bytes()
        return None

    async def delete(self, key: str) -> bool:
        self._validate_key(key)
        path = self._resolve(key)
        if path.exists():
            path.unlink()
            return True
        return False

    async def url(self, key: str) -> str:
        return f"/storage/{key.lstrip('/')}"

    def _resolve(self, key: str) -> Path:
        norm = self._normalise_path(key)
        resolved = (self._base / norm).resolve()
        if not str(resolved).startswith(str(self._base)):
            raise ValueError(f"Path traversal detected: {key}")
        return resolved
