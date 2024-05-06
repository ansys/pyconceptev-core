PyConceptEV-Core
================
|pyansys| |MIT| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |python| image:: https://img.shields.io/pypi/pyversions/ansys-conceptev-core?logo=pypi
   :target: TBD
   :alt: Python

.. |pypi| image:: https://img.shields.io/pypi/v/ansys-conceptev-core.svg?logo=python&logoColor=white
   :target: TBD
   :alt: PyPI

.. |downloads| image:: https://img.shields.io/pypi/dm/ansys-conceptev-core.svg
   :target: TBD
   :alt: PyPI Downloads

.. |codecov| image:: TBD
   :target: TBD
   :alt: Codecov

.. |GH-CI| image:: TBD
   :target: TBD
   :alt: GH-CI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black

.. |pre-commit| image:: TBD
   :target: TBD
   :alt: pre-commit.ci

.. contents::

Overview
--------

PyConceptEV-Core is a Python client library for the Ansys ConceptEV service.


Installation
------------

Two installation modes are provided: user and developer.

Install in user mode
^^^^^^^^^^^^^^^^^^^^

Before installing PyConceptEV-Core, make sure that you have the latest version
of `pip`_ by running this command:

.. code:: bash

   python -m pip install -U pip

Then, install PyConceptEV-Core with this command:

.. code:: bash

   python -m pip pip install ansys-conceptev-core

Install in development mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Installing PyConceptEV-Core in developer mode allows
you to modify the source and enhance it.

Before contributing to the project, see to the `PyAnsys developer's guide`_.

To install PyConceptEV-Core in developer mode, perform these steps:

#. Clone the repository and move into it:

.. code:: bash

   git clone https://github.com/ansys-internal/pyconceptev-core
   cd pyconceptev-core

#. Create a fresh-clean Python environment and activate it:

.. code:: bash

   # Create a virtual environment
   python -m venv .venv

   # Activate it in a POSIX system
   source .venv/bin/activate

   # Activate it in Windows CMD environment
   .venv\Scripts\activate.bat

   # Activate it in Windows Powershell
   .venv\Scripts\Activate.ps1

#. Make sure that you have the latest required build system and documentation, testing, and CI tools:

   .. code:: bash

      python -m pip install -U pip poetry tox

#. Install the project in editable mode:

   .. code:: bash

      poetry install

#. Finally, verify your development installation by running this command:

   .. code:: bash

      tox


Testing
-------

This project takes advantage of `tox`_. This tool lets you automate common
development tasks (similar to Makefile), but it is oriented towards Python
development.

Using tox
^^^^^^^^^

As Makefile has rules, `tox`_ has environments. In fact, the tool creates its
own virtual environment so that anything being tested is isolated from the project
to guarantee the project's integrity.

The following environments commands are provided:

- **tox -e style**: Checks for coding style quality.
- **tox -e py**: Cchecks for unit tests.
- **tox -e py-coverage**: Checks for unit testing and code coverage.
- **tox -e doc**: Checks for the documentation-building process.


Raw testing
^^^^^^^^^^^

If required, from the command line, you can always call style commands, such as
`black`_, `isort`_, and `flake8`_, or unit testing commands such as `pytest`_. However,
running these commands does not guarantee that your project is being tested in an isolated
environment, which is the reason why tools like `tox`_ exist.


A note on pre-commit
^^^^^^^^^^^^^^^^^^^^

The style checks take advantage of `pre-commit`_. Developers are not forced but
encouraged to install this tool by running this commandd:

.. code:: bash

   python -m pip install pre-commit && pre-commit install


Documentation
-------------

For building documentation, you can run the usual rules provided in the
`Sphinx`_ Makefile:

.. code:: bash

   # In Linux environment
   make -C doc/ html && your_browser_name doc/html/index.html

   # In Windows environment
   .\doc\make.bat html && your_browser_name doc/html/index.html

However, the recommended way of checking documentation integrity is using ``tox``:

.. code:: bash

   tox -e doc && your_browser_name .tox/doc_out/index.html


Distributing
------------

If you would like to create either source or wheel files, run these commands to
install the building requirements and then execute the build module:

.. code:: bash

   poetry install --with build
   python -m build
   python -m twine check dist/*


.. LINKS AND REFERENCES
.. _black: https://github.com/psf/black
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _pip: https://pypi.org/project/pip/
.. _pre-commit: https://pre-commit.com/
.. _PyAnsys developer's guide: https://dev.docs.pyansys.com/
.. _pytest: https://docs.pytest.org/en/stable/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _tox: https://tox.wiki/
