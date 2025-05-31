Usage Guide
===========

This guide introduces the core usage patterns of `darca-storage`, including how to create
a `StorageClient`, perform file operations, and leverage session-aware metadata securely.

----

Create a StorageClient
-----------------------

The `StorageConnectorFactory` resolves URL-based storage targets into secure, ready-to-use clients.

.. code-block:: python

    from darca_storage.factory import StorageConnectorFactory

    client = await StorageConnectorFactory.from_url("file:///tmp/my-data")

This guarantees a `StorageClient` backed by a `ScopedFileBackend`, which confines all paths
to the declared root directory.

----

Perform File Operations
-----------------------

Each operation is asynchronous and works with either text or binary content.

.. code-block:: python

    await client.write("notes.txt", content="hello world")
    text = await client.read("notes.txt")
    print(text)

    exists = await client.exists("notes.txt")
    await client.rename("notes.txt", "archived/hello.txt")

    await client.mkdir("logs")
    await client.rmdir("logs")

    await client.delete("archived/hello.txt")

----

Use Binary Files
----------------

Set the `binary=True` flag when working with bytes.

.. code-block:: python

    await client.write("data.bin", content=b"\x00\xFF", binary=True)
    content = await client.read("data.bin", binary=True)
    assert isinstance(content, bytes)

----

Session Metadata
----------------

Session context (e.g. repository name, storage path, tags) is propagated through `StorageClient`.

.. code-block:: python

    context = client.context()
    print(context["session_metadata"])

----

Credential Support
------------------

If provided, credentials are injected automatically into the connector and exposed securely:

.. code-block:: python

    client = await StorageConnectorFactory.from_url(
        "file:///var/data",
        credentials={"posix_user": "backup"},
        session_metadata={"request_id": "abc-123"},
    )

    print(client.credentials)      # {'posix_user': 'backup'}
    print(client.context()["credentials"])  # {'posix_user': '***'}

----

Path Security: ScopedFileBackend
--------------------------------

Every file path is confined to a declared root directory. Any attempt to escape (e.g. via `../`) raises an error:

.. code-block:: python

    await client.write("../etc/passwd", "oops")

.. error::

    StorageClientPathViolation: Access to '/etc/passwd' is outside the storage base path

----

Flush and Refresh Hooks
-----------------------

Hooks for future extension (e.g., buffering, auth refresh):

.. code-block:: python

    await client.flush()    # no-op unless implemented
    await client.refresh()  # e.g. for cloud token renewal
