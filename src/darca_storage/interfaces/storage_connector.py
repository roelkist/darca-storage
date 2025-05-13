from abc import ABC, abstractmethod
from typing import Optional

from darca_storage.client import StorageClient


class StorageConnector(ABC):
    """
    Abstract interface for connecting to a storage backend.

    Implementations must:
    - Connect and return a scoped StorageClient rooted in a base path
    - Verify the backend is available
    - Verify that access is permitted
    """

    @abstractmethod
    def connect(self) -> StorageClient:
        """
        Return a StorageClient instance scoped to the backend and base path.

        Raises:
            RuntimeError: if the connection cannot be established
        """
        pass

    @abstractmethod
    def verify_connection(self) -> bool:
        """
        Return True if the backend is reachable (e.g., path exists, endpoint responds).
        """
        pass

    @abstractmethod
    def verify_access(
        self,
        user: Optional[str] = None,
        permissions: Optional[int] = None,
    ) -> bool:
        """
        Return True if the user has access to the root/base of the storage.

        Args:
            user (Optional[str]): User context for ownership verification.
            permissions (Optional[int]): Permission bits to apply when testing access.
        """
        pass
