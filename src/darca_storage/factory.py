# src/darca_storage/factory.py
# License: MIT
"""
StorageConnectorFactory

Maps a URL (e.g. *file:///data*) to a concrete **async** StorageConnector
implementation.  Creating the connector is synchronous and cheap; callers
will `await connector.connect()` to obtain the async `StorageClient`.
"""

from __future__ import annotations

import os
from urllib.parse import unquote, urlparse
import asyncio

from darca_storage.client import StorageClient
from darca_storage.connectors.local import LocalStorageConnector

class StorageConnectorFactory:  # noqa: D101
    @staticmethod
    async def from_url(url: str) -> StorageClient:
        """
        Parse *url* and return the corresponding **async** StorageConnector.

        Supported schemes:
            • file://  - local filesystem path
        """
        parsed = urlparse(url)
        scheme = parsed.scheme
        path = unquote(parsed.path)

        if scheme == "file":
            # Handle edge-cases like file:/tmp or file://localhost/tmp
            base_path = os.path.abspath(path or "/")
            connector = LocalStorageConnector(base_path=base_path)
            backend = await connector.connect()
            return StorageClient(backend=backend)

        # Placeholder for future back-ends (e.g., s3://, mem://)
        raise ValueError(f"Unsupported storage scheme: {scheme}")
