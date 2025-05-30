# src/darca_storage/connectors/local.py
# License: MIT
"""
Async connector for a local-filesystem backend.

• Performs reachability and access probes without blocking the event-loop
  (`asyncio.to_thread`).
• Returns a ready-scoped *async* `StorageClient`.
"""

from __future__ import annotations

import asyncio
import os
from typing import Optional

from darca_file_utils.directory_utils import DirectoryUtils, DirectoryUtilsException
from darca_file_utils.file_utils import FileUtils, FileUtilsException
from darca_storage.backends.local_file_backend import LocalFileBackend
from darca_storage.interfaces.storage_connector import StorageConnector
from darca_storage.decorators.scoped_backend import ScopedFileBackend


class LocalStorageConnector(StorageConnector):  # noqa: D101
    def __init__(self, base_path: str) -> None:
        if not base_path:
            raise ValueError("A base_path must be provided for LocalStorageConnector.")
        self._base_path: str = os.path.abspath(base_path)


    async def connect(self) -> LocalFileBackend:
        if not await self.verify_connection():
            raise RuntimeError(f"Local storage path '{self._base_path}' is not reachable.")
        if not await self.verify_access():
            raise PermissionError(f"Access to '{self._base_path}' is denied.")
        
        return ScopedFileBackend(backend=LocalFileBackend(), base_path=self._base_path)


    async def verify_connection(self) -> bool:
        """True if the directory exists."""
        return await asyncio.to_thread(DirectoryUtils.directory_exist, self._base_path)

    async def verify_access(
        self,
        *,
        user: Optional[str] = None,
        permissions: Optional[int] = None,
    ) -> bool:
        """Attempt mkdir / touch / rm to prove we have RW access."""
        try:
            # Ensure root directory exists (mkdir may be needed the first time)
            await asyncio.to_thread(
                self._ensure_dir, user=user, permissions=permissions
            )

            # Probe write / delete
            test_file = os.path.join(self._base_path, f".access_check_{os.getpid()}")
            await asyncio.to_thread(
                FileUtils.write_file,
                file_path=test_file,
                content="ok",
                binary=False,
                permissions=permissions,
                user=user,
            )
            await asyncio.to_thread(FileUtils.remove_file, test_file)
            return True
        except (DirectoryUtilsException, FileUtilsException):
            return False


    def _ensure_dir(self, *, user: Optional[str], permissions: Optional[int]) -> None:
        if not DirectoryUtils.directory_exist(self._base_path):
            DirectoryUtils.create_directory(
                path=self._base_path,
                permissions=permissions,
                user=user,
            )


    @property
    def base_path(self) -> str:  # noqa: D401
        """Absolute root directory this connector targets."""
        return self._base_path
