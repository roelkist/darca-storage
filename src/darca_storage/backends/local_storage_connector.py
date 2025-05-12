import os
from typing import Optional

from darca_space_manager import config
from darca_space_manager.core.interfaces.storage_connector import StorageConnector
from darca_space_manager.core.backends.local_file_backend import LocalFileBackend
from darca_space_manager.core.interfaces.file_backend import FileBackend
from darca_space_manager.core.space_registry import SpaceMetadataRegistry


class LocalStorageConnector(StorageConnector):
    """
    Connector for a local filesystem backend. Validates base path availability and write access.
    """

    def __init__(self, base_path: Optional[str] = None):
        config.ensure_directories_exist()  # 🔧 ensure all expected dirs exist

        registry_base = SpaceMetadataRegistry().load_registry().get("base_path")
        self._base_path = base_path or registry_base or os.path.expanduser("~/.local/share/darca_space/spaces")

        self._backend = LocalFileBackend()

    def connect(self) -> FileBackend:
        if not self.verify_connection():
            raise RuntimeError(f"Local storage path '{self._base_path}' is not reachable.")
        if not self.verify_access():
            raise PermissionError(f"Current user does not have access to '{self._base_path}'.")
        return self._backend

    def verify_connection(self) -> bool:
        return os.path.exists(self._base_path) and os.path.isdir(self._base_path)

    def verify_access(self, user: Optional[str] = None) -> bool:
        try:
            test_file = os.path.join(self._base_path, f".access_check_{os.getpid()}")
            with open(test_file, "w") as f:
                f.write("ok")
            os.remove(test_file)
            return True
        except Exception:
            return False

    @property
    def base_path(self) -> str:
        return self._base_path
