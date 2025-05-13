import os
from typing import List, Union, Optional
from darca_storage.interfaces.file_backend import FileBackend
from darca_storage.exceptions import StorageClientPathViolation

class StorageClient:
    """
    StorageClient provides scoped access to a FileBackend, rooted at a base_path.
    All operations are relative to this base path.
    """

    def __init__(self, backend: FileBackend, base_path: str):
        self._backend = backend
        self._base_path = os.path.abspath(base_path)

    def _full_path(self, relative_path: str) -> str:
        full = os.path.realpath(os.path.abspath(os.path.join(self._base_path, relative_path)))
        base = os.path.realpath(self._base_path)

        if not full.startswith(base + os.sep) and full != base:
            raise StorageClientPathViolation(
                attempted_path=full,
                base_path=base
            )

        return full

    def read(self, relative_path: str, binary: bool = False) -> Union[str, bytes]:
        return self._backend.read(self._full_path(relative_path), binary=binary)

    def write(
        self,
        relative_path: str,
        content: Union[str, bytes],
        *,
        permissions: Optional[int] = None,
        user: Optional[str] = None
    ):
        self._backend.write(
            path=self._full_path(relative_path),
            content=content,
            permissions=permissions,
            user=user
        )

    def delete(self, relative_path: str):
        self._backend.delete(self._full_path(relative_path))

    def exists(self, relative_path: str) -> bool:
        return self._backend.exists(self._full_path(relative_path))

    def list(self, relative_path: str = ".", recursive: bool = False) -> List[str]:
        return self._backend.list(self._full_path(relative_path), recursive=recursive)

    def mkdir(
        self,
        relative_path: str,
        parents: bool = True,
        *,
        permissions: Optional[int] = None,
        user: Optional[str] = None
    ):
        self._backend.mkdir(
            path=self._full_path(relative_path),
            parents=parents,
            permissions=permissions,
            user=user
        )

    def rmdir(self, relative_path: str):
        self._backend.rmdir(self._full_path(relative_path))

    def rename(self, src_relative: str, dest_relative: str):
        self._backend.rename(
            self._full_path(src_relative),
            self._full_path(dest_relative)
        )

    def stat_mtime(self, relative_path: str) -> float:
        return self._backend.stat_mtime(self._full_path(relative_path))

    @property
    def base_path(self) -> str:
        return self._base_path

    @property
    def backend(self) -> FileBackend:
        return self._backend
