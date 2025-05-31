# tests/conftest.py

import shutil
import tempfile

import pytest


@pytest.fixture(scope="function")
def temp_storage_dir():
    """
    Creates and cleans up a temporary directory for storage backend tests.
    """
    base = tempfile.mkdtemp(prefix="darca_storage_test_")
    yield base
    shutil.rmtree(base, ignore_errors=True)
