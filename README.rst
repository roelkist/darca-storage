darca-storage
===================

Storage intance with file operation support for multiple backends.

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

📦 Installation
---------------

.. code-block:: bash

   pip install darca-storage

Or using Poetry:

.. code-block:: bash

   poetry add darca-storage

📚 Documentation
----------------

Visit the full documentation:

👉 https://roelkist.github.io/darca-storage/

To build locally:

.. code-block:: bash

   make docs

🧪 Testing
----------

Run all tests using:

.. code-block:: bash

   make test

Coverage and reports:

- Generates `coverage.svg` badge
- Stores HTML output in `htmlcov/`
- Fully parallel test support with `xdist`

🤝 Contributing
---------------

We welcome all contributions!

- Create a new **branch** from `main`
- Use PRs to submit changes
- You can also open feature requests or issues using our GitHub templates

See `CONTRIBUTING.rst` for detailed guidelines.

📄 License
----------

This project is licensed under the MIT License.
See `LICENSE <https://github.com/roelkist/darca-storage/blob/main/LICENSE>`_ for details.
