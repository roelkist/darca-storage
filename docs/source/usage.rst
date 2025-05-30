Usage Guide
===========

This guide demonstrates how to use `darca-storage` in real-world applications.

Quickstart
----------

Install:

.. code-block:: bash

    pip install darca-storage

Get a storage client for the local filesystem:

.. code-block:: python

    from darca_storage.factory import StorageConnectorFactory

    async def init_client():
        client = await StorageConnectorFactory.from_url("file:///tmp/app-storage")
        await client.write("welcome.txt", "Hello Darca!")
        print(await client.read("welcome.txt"))

All client paths are **scoped** to the base directory you provide.
Escape attempts like `../../etc/passwd` will be rejected.

API Overview
------------

Once connected, the client exposes all core methods:

.. code-block:: python

    await client.write("file.txt", "data")
    exists = await client.exists("file.txt")
    content = await client.read("file.txt")
    await client.rename("file.txt", "renamed.txt")
    await client.delete("renamed.txt")

Directory management:

.. code-block:: python

    await client.mkdir("data/logs", parents=True)
    files = await client.list("data", recursive=True)
    await client.rmdir("data/logs")

Session Metadata
----------------

`StorageClient` captures session context, useful for inspection or auditing:

.. code-block:: python

    print(client.user)  # 'your-username' (optional)
    print(client.session)  # {'scheme': 'file', 'base_path': '/tmp/app-storage'}

    print(client.context())
    # {
    #   'user': 'your-username',
    #   'session_metadata': {'scheme': 'file', 'base_path': ...},
    #   'backend_type': 'ScopedFileBackend'
    # }

Testing
-------

You can use a real `file://` temp directory for integration tests, or mock the backend for unit tests:

.. code-block:: python

    from unittest.mock import AsyncMock
    from darca_storage.client import StorageClient

    backend = AsyncMock()
    backend.read.return_value = "mock"
    client = StorageClient(backend=backend)

    assert await client.read("x") == "mock"

Future Extensions
-----------------

Planned enhancements include:

- `s3://` for AWS S3
- `mem://` for ephemeral storage
- `presign_url()` for web access
- Token-aware `refresh()` for cloud credentials

All connectors will be discoverable via `StorageConnectorFactory.from_url(...)`.

