import os
from urllib.parse import urlparse, unquote

from darca_storage.interfaces.storage_connector import StorageConnector
from darca_storage.connectors.local import LocalStorageConnector


class StorageConnectorFactory:
    """
    Factory for instantiating StorageConnector implementations from URLs.

    Example:
        file:///tmp/data → LocalStorageConnector(base_path="/tmp/data")
    """

    @staticmethod
    def from_url(url: str) -> StorageConnector:
        parsed = urlparse(url)

        scheme = parsed.scheme
        path = unquote(parsed.path)

        if scheme == "file":
            # Handle edge cases like file:/tmp or file://localhost/tmp
            base_path = os.path.abspath(path or "/")
            return LocalStorageConnector(base_path=base_path)

        # Placeholder for future backends (e.g., s3://, mem://)
        raise ValueError(f"Unsupported storage scheme: {scheme}")
