from __future__ import annotations

from darca_storage.interfaces.file_backend import FileBackend


class StorageClient:
    """
    Thin wrapper over a FileBackend.
    Meant for high-level features layered over storage access.
    """

    def __init__(self, backend: FileBackend) -> None:
        self._backend = backend
     
    def __getattr__(self, name):
        # Delegate unknown methods to backend (transparent proxy)
        return getattr(self._backend, name)

    @property
    def backend(self) -> FileBackend:
        return self._backend
