"""Storage backends for CARE workspaces."""

from .base import StorageBackend
from .local import LocalStorage


def create_storage(storage_type: str, **kwargs) -> StorageBackend:
    """Factory for storage backends.

    Args:
        storage_type: "local" or "gdrive"
        For local: root="/path/to/workspace/root"
        For gdrive: folder_id="...", credentials="path/to/creds.json" (optional)
    """
    if storage_type == "local":
        return LocalStorage(kwargs["root"])
    elif storage_type == "gdrive":
        from .gdrive import GoogleDriveStorage
        return GoogleDriveStorage(
            folder_id=kwargs["folder_id"],
            credentials_path=kwargs.get("credentials"),
        )
    else:
        raise ValueError(f"Unknown storage type: {storage_type}")
