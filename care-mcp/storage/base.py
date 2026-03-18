"""Abstract storage backend for CARE workspaces."""

from abc import ABC, abstractmethod
import posixpath


class StorageBackend(ABC):
    """Abstract storage backend. All paths are POSIX-style strings relative to the storage root."""

    @abstractmethod
    def exists(self, path: str) -> bool: ...

    @abstractmethod
    def is_dir(self, path: str) -> bool: ...

    @abstractmethod
    def is_file(self, path: str) -> bool: ...

    @abstractmethod
    def mkdir(self, path: str) -> None:
        """Create directory and all parents."""

    @abstractmethod
    def read_text(self, path: str) -> str: ...

    @abstractmethod
    def write_text(self, path: str, content: str) -> None:
        """Write text to file. Creates parent directories if needed."""

    @abstractmethod
    def list_dir(self, path: str) -> list[str]:
        """List immediate child names in a directory, sorted."""

    @abstractmethod
    def list_dir_info(self, path: str) -> list[dict]:
        """List immediate children with metadata: [{name: str, is_dir: bool}], sorted by (not is_dir, name)."""

    @abstractmethod
    def glob(self, path: str, pattern: str) -> list[str]:
        """Glob within a single directory. Returns paths relative to storage root."""

    @abstractmethod
    def rglob(self, path: str, pattern: str) -> list[str]:
        """Recursive glob. Returns paths relative to storage root."""

    @abstractmethod
    def resolve(self, path: str) -> str:
        """Return a canonical/absolute identifier for this path."""

    def join(self, *parts: str) -> str:
        """Join path components."""
        return posixpath.join(*parts)

    def parent(self, path: str) -> str:
        """Get parent directory path."""
        return posixpath.dirname(path)

    def name(self, path: str) -> str:
        """Get filename component."""
        return posixpath.basename(path)

    def relative_to(self, path: str, base: str) -> str:
        """Get path relative to base."""
        return posixpath.relpath(path, base)
