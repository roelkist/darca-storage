# tests/test_factory.py

import os
import pytest

from darca_storage.factory import StorageConnectorFactory
from darca_storage.client import StorageClient
from darca_storage.decorators.scoped_backend import ScopedFileBackend


@pytest.mark.asyncio
async def test_factory_returns_scoped_client(temp_storage_dir):
    url = f"file://{temp_storage_dir}"

    client = await StorageConnectorFactory.from_url(url)

    assert isinstance(client, StorageClient)
    assert isinstance(client.backend, ScopedFileBackend)

    # Write and read test
    await client.write("test.txt", "hello")
    content = await client.read("test.txt")
    assert content == "hello"

    # Context includes base path
    context = client.context()
    assert context["session_metadata"]["base_path"] == os.path.abspath(temp_storage_dir)


@pytest.mark.asyncio
async def test_factory_rejects_unsupported_scheme():
    with pytest.raises(ValueError) as exc:
        await StorageConnectorFactory.from_url("ftp://localhost/data")

    assert "Unsupported storage scheme" in str(exc.value)
