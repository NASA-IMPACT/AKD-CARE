"""Google Drive storage backend for CARE workspaces.

Uses a Google Drive folder as the storage root. All files are plain text (Markdown).
Requires google-api-python-client and google-auth:
    uv pip install google-api-python-client google-auth
"""

import fnmatch
import io
import os
import posixpath

from loguru import logger

from .base import StorageBackend


class GoogleDriveStorage(StorageBackend):
    """Storage backend backed by Google Drive.

    Uses a shared folder as the root. All paths are POSIX-style strings
    relative to that folder (e.g., "my_project/context/terminology/rain.md").
    """

    def __init__(self, folder_id: str, credentials_path: str | None = None):
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        self._root_id = folder_id

        if credentials_path:
            creds = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=["https://www.googleapis.com/auth/drive"],
            )
        else:
            from google.auth import default
            creds, _ = default(scopes=["https://www.googleapis.com/auth/drive"])

        self._service = build("drive", "v3", credentials=creds)
        self._cache: dict[str, dict] = {}  # path -> {id, is_dir, name}
        self._cache[""] = {"id": self._root_id, "is_dir": True, "name": ""}
        self._warm_cache()

    def _warm_cache(self) -> None:
        """Eagerly walk the entire folder tree to populate the cache."""
        self._walk_folder("", self._root_id)
        logger.info(f"Google Drive cache warmed: {len(self._cache)} entries")

    def _walk_folder(self, prefix: str, folder_id: str) -> None:
        """Recursively list folder contents and cache them."""
        page_token = None
        while True:
            resp = self._service.files().list(
                q=f"'{folder_id}' in parents and trashed=false",
                fields="nextPageToken, files(id, name, mimeType)",
                pageSize=1000,
                pageToken=page_token,
            ).execute()

            for item in resp.get("files", []):
                is_dir = item["mimeType"] == "application/vnd.google-apps.folder"
                path = posixpath.join(prefix, item["name"]) if prefix else item["name"]
                self._cache[path] = {"id": item["id"], "is_dir": is_dir, "name": item["name"]}
                if is_dir:
                    self._walk_folder(path, item["id"])

            page_token = resp.get("nextPageToken")
            if not page_token:
                break

    def _resolve_id(self, path: str) -> str | None:
        """Get the Drive file ID for a path, or None if not cached."""
        if path in self._cache:
            return self._cache[path]["id"]
        return None

    def _ensure_parent(self, path: str) -> str:
        """Ensure parent directory exists, return its ID."""
        parent = posixpath.dirname(path)
        if not parent:
            return self._root_id
        if parent in self._cache:
            return self._cache[parent]["id"]
        # Recursively create parents
        grandparent_id = self._ensure_parent(parent)
        folder_name = posixpath.basename(parent)
        folder = self._service.files().create(
            body={
                "name": folder_name,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [grandparent_id],
            },
            fields="id",
        ).execute()
        self._cache[parent] = {"id": folder["id"], "is_dir": True, "name": folder_name}
        return folder["id"]

    def exists(self, path: str) -> bool:
        return path in self._cache

    def is_dir(self, path: str) -> bool:
        entry = self._cache.get(path)
        return entry is not None and entry["is_dir"]

    def is_file(self, path: str) -> bool:
        entry = self._cache.get(path)
        return entry is not None and not entry["is_dir"]

    def mkdir(self, path: str) -> None:
        if path in self._cache:
            return
        parts = path.split("/")
        current = ""
        for part in parts:
            current = posixpath.join(current, part) if current else part
            if current not in self._cache:
                parent_id = self._resolve_id(posixpath.dirname(current)) or self._root_id
                folder = self._service.files().create(
                    body={
                        "name": part,
                        "mimeType": "application/vnd.google-apps.folder",
                        "parents": [parent_id],
                    },
                    fields="id",
                ).execute()
                self._cache[current] = {"id": folder["id"], "is_dir": True, "name": part}

    def read_text(self, path: str) -> str:
        file_id = self._resolve_id(path)
        if not file_id:
            raise FileNotFoundError(f"File not found in Google Drive: {path}")
        content = self._service.files().get_media(fileId=file_id).execute()
        if isinstance(content, bytes):
            return content.decode("utf-8")
        return str(content)

    def write_text(self, path: str, content: str) -> None:
        from googleapiclient.http import MediaInMemoryUpload

        media = MediaInMemoryUpload(content.encode("utf-8"), mimetype="text/markdown")
        file_id = self._resolve_id(path)

        if file_id:
            self._service.files().update(fileId=file_id, media_body=media).execute()
        else:
            parent_id = self._ensure_parent(path)
            name = posixpath.basename(path)
            result = self._service.files().create(
                body={"name": name, "parents": [parent_id]},
                media_body=media,
                fields="id",
            ).execute()
            self._cache[path] = {"id": result["id"], "is_dir": False, "name": name}

    def list_dir(self, path: str) -> list[str]:
        prefix = path + "/" if path else ""
        children = set()
        for cached_path in self._cache:
            if not cached_path.startswith(prefix) or cached_path == path:
                continue
            rest = cached_path[len(prefix):]
            if "/" not in rest:
                children.add(rest)
        return sorted(children)

    def list_dir_info(self, path: str) -> list[dict]:
        prefix = path + "/" if path else ""
        children = {}
        for cached_path, entry in self._cache.items():
            if not cached_path.startswith(prefix) or cached_path == path:
                continue
            rest = cached_path[len(prefix):]
            if "/" not in rest:
                children[rest] = entry["is_dir"]
        result = [{"name": name, "is_dir": is_dir} for name, is_dir in children.items()]
        return sorted(result, key=lambda x: (not x["is_dir"], x["name"]))

    def glob(self, path: str, pattern: str) -> list[str]:
        prefix = path + "/" if path else ""
        results = []
        for cached_path in sorted(self._cache):
            if not cached_path.startswith(prefix) or cached_path == path:
                continue
            rest = cached_path[len(prefix):]
            if "/" not in rest and fnmatch.fnmatch(rest, pattern):
                results.append(cached_path)
        return results

    def rglob(self, path: str, pattern: str) -> list[str]:
        prefix = path + "/" if path else ""
        results = []
        for cached_path in sorted(self._cache):
            if not cached_path.startswith(prefix) or cached_path == path:
                continue
            rest = cached_path[len(prefix):]
            if fnmatch.fnmatch(rest, pattern) or fnmatch.fnmatch(posixpath.basename(rest), pattern):
                results.append(cached_path)
        return results

    def resolve(self, path: str) -> str:
        file_id = self._resolve_id(path) or "unknown"
        return f"https://drive.google.com/drive/folders/{file_id}" if self.is_dir(path) else f"https://drive.google.com/file/d/{file_id}"
