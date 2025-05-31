Darca Storage
=============

Async-first, secure, and extensible storage backend abstraction for the Darca ecosystem.

`darca-storage` provides a clean interface for reading and writing to structured storage backends —
local, cloud, or custom — with support for path confinement, credential injection, and session-aware logic.

----

|Build Status| |Deploy Status| |CodeCov| |Formatting| |License| |PyPi Version| |Docs|

.. |Build Status| image:: https://github.com/roelkist/darca-storage/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/roelkist/darca-storage/actions
.. |Deploy Status| image:: https://github.com/roelkist/darca-storage/actions/workflows/cd.yml/badge.svg
   :target: https://github.com/roelkist/darca-storage/actions
.. |Codecov| image:: https://codecov.io/gh/roelkist/darca-storage/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/roelkist/darca-storage
   :alt: Codecov
.. |Formatting| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black code style
.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
.. |PyPi Version| image:: https://img.shields.io/pypi/v/darca-storage
   :target: https://pypi.org/project/darca-storage/
   :alt: PyPi
.. |Docs| image:: https://img.shields.io/github/deployments/roelkist/darca-storage/github-pages
   :target: https://roelkist.github.io/darca-storage/
   :alt: GitHub Pages

----

Features
--------

- ✅ Async-compatible `FileBackend` interface
- 🔐 Scoped access via `ScopedFileBackend`
- 🧠 Session-aware `StorageClient` with observability
- 🔌 Pluggable storage connectors (e.g., file://)
- 🔄 Credential and user context propagation
- 🧪 Easy to test and extend

----

📦 Installation
---------------

.. code-block:: bash

   pip install darca-storage

Or using Poetry:

.. code-block:: bash

   poetry add darca-storage

----

Quick Example
-------------

.. code-block:: python

    from darca_storage.factory import StorageConnectorFactory

    client = await StorageConnectorFactory.from_url("file:///tmp/darca")

    await client.write("hello.txt", content="Hello Darca!")
    text = await client.read("hello.txt")
    print(text)

----

Security by Default
-------------------

All paths are resolved via `ScopedFileBackend`, which:

- Normalizes and confines all access to a declared `base_path`
- Prevents path traversal (e.g., `../../etc/passwd`)
- Raises `StorageClientPathViolation` if the boundary is violated

----

Extending
---------

Implement a new backend:

.. code-block:: python

    class MyBackend(FileBackend):
        async def read(self, path: str, *, binary=False) -> Union[str, bytes]:
            ...

Implement a new connector:

.. code-block:: python

    class MyConnector(StorageConnector):
        async def connect(self) -> FileBackend:
            return ScopedFileBackend(...)

Then register your scheme inside `StorageConnectorFactory`.

----

📚 Documentation
----------------

Visit the full documentation:

👉 https://roelkist.github.io/darca-storage/

To build locally:

.. code-block:: bash

   make docs

----

🧪 Testing
----------

Run all tests using:

.. code-block:: bash

   make test

Coverage and reports:

- Generates `coverage.svg` badge
- Stores HTML output in `htmlcov/`
- Fully parallel test support with `xdist`

----

🤝 Contributing
---------------

We welcome all contributions!

- Create a new **branch** from `main`
- Use PRs to submit changes
- You can also open feature requests or issues using our GitHub templates

See `CONTRIBUTING.rst` for detailed guidelines.

----

📄 License
----------

This project is licensed under the MIT License.
See `LICENSE <https://github.com/roelkist/darca-storage/blob/main/LICENSE>`_ for details.
