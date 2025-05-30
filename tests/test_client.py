# tests/test_client.py

import pytest
from unittest.mock import AsyncMock, MagicMock

from darca_storage.client import StorageClient


@pytest.fixture
def mock_backend():
    backend = MagicMock()

    backend.read = AsyncMock(return_value="mocked-content")
    backend.write = AsyncMock()
    backend.delete = AsyncMock()
    backend.exists = AsyncMock(return_value=True)
    backend.list = AsyncMock(return_value=["a.txt", "b.txt"])
    backend.mkdir = AsyncMock()
    backend.rmdir = AsyncMock()
    backend.rename = AsyncMock()
    backend.stat_mtime = AsyncMock(return_value=1234567890.0)

    return backend


@pytest.fixture
def client(mock_backend):
    return StorageClient(
        backend=mock_backend,
        session_metadata={"env": "test"},
        user="test-user"
    )


@pytest.mark.asyncio
async def test_read(client):
    result = await client.read("file.txt")
    assert result == "mocked-content"
    client.backend.read.assert_awaited_once_with(relative_path="file.txt", binary=False)


@pytest.mark.asyncio
async def test_write(client):
    await client.write("data.txt", "hello")
    client.backend.write.assert_awaited_once_with(
        relative_path="data.txt",
        content="hello",
        binary=False,
        permissions=None,
        user="test-user",
    )


@pytest.mark.asyncio
async def test_delete(client):
    await client.delete("remove.txt")
    client.backend.delete.assert_awaited_once_with(relative_path="remove.txt")


@pytest.mark.asyncio
async def test_exists(client):
    assert await client.exists("maybe.txt") is True
    client.backend.exists.assert_awaited_once_with(relative_path="maybe.txt")


@pytest.mark.asyncio
async def test_list(client):
    files = await client.list("folder", recursive=True)
    assert files == ["a.txt", "b.txt"]
    client.backend.list.assert_awaited_once_with(relative_path="folder", recursive=True)


@pytest.mark.asyncio
async def test_mkdir(client):
    await client.mkdir("newdir")
    client.backend.mkdir.assert_awaited_once_with(
        relative_path="newdir",
        parents=True,
        permissions=None,
        user="test-user",
    )


@pytest.mark.asyncio
async def test_rmdir(client):
    await client.rmdir("trash")
    client.backend.rmdir.assert_awaited_once_with(relative_path="trash")


@pytest.mark.asyncio
async def test_rename(client):
    await client.rename("src.txt", "dst.txt")
    client.backend.rename.assert_awaited_once_with(
        src_relative="src.txt",
        dest_relative="dst.txt"
    )


@pytest.mark.asyncio
async def test_stat_mtime(client):
    mtime = await client.stat_mtime("data.txt")
    assert mtime == 1234567890.0
    client.backend.stat_mtime.assert_awaited_once_with(relative_path="data.txt")


@pytest.mark.asyncio
async def test_session_properties(client):
    assert client.user == "test-user"
    assert client.session == {"env": "test"}


@pytest.mark.asyncio
async def test_context(client):
    ctx = client.context()
    assert ctx["user"] == "test-user"
    assert ctx["session_metadata"]["env"] == "test"
    assert "backend_type" in ctx


@pytest.mark.asyncio
async def test_refresh_is_noop(client):
    await client.refresh()  # No exception, nothing to assert


@pytest.mark.asyncio
async def test_flush_is_noop(client):
    await client.flush()  # No exception, nothing to assert


@pytest.mark.asyncio
async def test_presign_url_returns_none(client):
    assert await client.presign_url("nope.txt", expires_in=300) is None
