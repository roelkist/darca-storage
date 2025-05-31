# tests/test_scoped_backend.py

import os

import pytest

from darca_storage.backends.local_file_backend import LocalFileBackend
from darca_storage.decorators.scoped_backend import ScopedFileBackend
from darca_storage.exceptions import StorageClientPathViolation


@pytest.mark.asyncio
async def test_scoped_backend_blocks_escape(temp_storage_dir):
    backend = ScopedFileBackend(LocalFileBackend(), base_path=temp_storage_dir)

    # Create a file inside the scope
    await backend.write("inside.txt", "ok")
    content = await backend.read("inside.txt")
    assert content == "ok"

    # Attempt escape using relative path
    with pytest.raises(StorageClientPathViolation):
        await backend.read("../outside.txt")


@pytest.mark.asyncio
async def test_scoped_backend_allows_nested_paths(temp_storage_dir):
    backend = ScopedFileBackend(LocalFileBackend(), base_path=temp_storage_dir)

    subdir = os.path.join("nested", "dir")
    filename = os.path.join(subdir, "file.txt")

    await backend.mkdir(subdir)
    await backend.write(filename, "data")

    assert await backend.exists(filename)
    assert await backend.read(filename) == "data"
