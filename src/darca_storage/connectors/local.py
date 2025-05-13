import os
from typing import Optional

from darca_storage.interfaces.storage_connector import StorageConnector
from darca_storage.backends.local_file_backend import LocalFileBackend
from darca_storage.client import StorageClient
from darca_file_utils.directory_utils import DirectoryUtils, DirectoryUtilsException
from darca_file_utils.file_utils import FileUtils, FileUtilsException


class LocalStorageConnector(StorageConnector):
    """
    Connector for a local filesystem backend.

    Produces a scoped StorageClient instance rooted in a specified base_path.
    """

    def __init__(self, base_path: str):
        if not base_path:
            raise ValueError("A base_path must be provided for LocalStorageConnector.")
        self._base_path = os.path.abspath(base_path)

    def connect(self) -> StorageClient:
        if not self.verify_connection():
            raise RuntimeError(f"Local storage path '{self._base_path}' is not reachable.")
        if not self.verify_access():
            raise PermissionError(f"Access to '{self._base_path}' is denied.")

        backend = LocalFileBackend()
        return StorageClient(backend=backend, base_path=self._base_path)

    def verify_connection(self) -> bool:
        try:
            return DirectoryUtils.directory_exist(self._base_path)
        except DirectoryUtilsException:
            return False

    def verify_access(
        self,
        user: Optional[str] = None,
        permissions: Optional[int] = None
    ) -> bool:
        try:
            if not DirectoryUtils.directory_exist(self._base_path):
                DirectoryUtils.create_directory(
                    path=self._base_path,
                    permissions=permissions,
                    user=user
                )

            test_file = os.path.join(self._base_path, f".access_check_{os.getpid()}")
            FileUtils.write_file(
                file_path=test_file,
                content="ok",
                permissions=permissions,
                user=user
            )
            FileUtils.remove_file(test_file)
            return True

        except (DirectoryUtilsException, FileUtilsException):
            return False

    @property
    def base_path(self) -> str:
        return self._base_path
