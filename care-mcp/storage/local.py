"""Local filesystem storage backend."""

import fnmatch
from pathlib import Path

from .base import StorageBackend


class LocalStorage(StorageBackend):
    """Storage backend backed by the local filesystem."""

    def __init__(self, root: str):
        self._root = Path(root)

    def _path(self, path: str) -> Path:
        if not path:
            return self._root
        return self._root / path

    def exists(self, path: str) -> bool:
        return self._path(path).exists()

    def is_dir(self, path: str) -> bool:
        return self._path(path).is_dir()

    def is_file(self, path: str) -> bool:
        return self._path(path).is_file()

    def mkdir(self, path: str) -> None:
        self._path(path).mkdir(parents=True, exist_ok=True)

    def read_text(self, path: str) -> str:
        return self._path(path).read_text()

    def write_text(self, path: str, content: str) -> None:
        p = self._path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)

    def list_dir(self, path: str) -> list[str]:
        return sorted(e.name for e in self._path(path).iterdir())

    def list_dir_info(self, path: str) -> list[dict]:
        entries = []
        for e in self._path(path).iterdir():
            entries.append({"name": e.name, "is_dir": e.is_dir()})
        return sorted(entries, key=lambda x: (not x["is_dir"], x["name"]))

    def glob(self, path: str, pattern: str) -> list[str]:
        base = self._path(path)
        results = []
        for p in sorted(base.glob(pattern)):
            results.append(str(p.relative_to(self._root)))
        return results

    def rglob(self, path: str, pattern: str) -> list[str]:
        base = self._path(path)
        results = []
        for p in sorted(base.rglob(pattern)):
            results.append(str(p.relative_to(self._root)))
        return results

    def resolve(self, path: str) -> str:
        return str(self._path(path).resolve())
