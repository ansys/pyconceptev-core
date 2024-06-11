.. _ref_contributing:

Contribute
##########

Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <https://dev.docs.pyansys.com/how-to/contributing.html>`_ topic
in the *PyAnsys developer's guide*. Ensure that you are thoroughly familiar
with this guide before attempting to contribute to PyConceptEV.

The following contribution information is specific to PyConceptEV.

Install in developer mode
-------------------------

Installing PyConceptEV in developer mode allows you to modify and enhance
the source.

#. Clone the repository and move into it:

   .. code:: bash

      git clone https://github.com/ansys/pyconceptev-core
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

#. Make sure that you have the latest required build system and documentation, testing,
   and CI tools:

   .. code:: bash

      python -m pip install -U pip poetry tox

#. Install the project in editable mode:

   .. code:: bash

      poetry install

#. Verify your development installation:

   .. code:: bash

      tox


Testing
-------

This project takes advantage of `tox`_. This tool lets you automate common
development tasks (similar to Makefile), but it is oriented towards Python
development.

Use ``tox``
^^^^^^^^^^^

As Makefile has rules, `tox`_ has environments. In fact, the tool creates its
own virtual environment so that anything being tested is isolated from the project
to guarantee the project's integrity.

The following environment commands are provided:

- **tox -e style**: Checks for coding style quality.
- **tox -e py**: Checks for unit tests.
- **tox -e py-coverage**: Checks for unit testing and code coverage.
- **tox -e doc**: Checks for the documentation-building process.


Perform raw testing
^^^^^^^^^^^^^^^^^^^

If required, from the command line, you can always call style commands, such as
`Black`_, `isort`_, and `Flake8`_, or unit testing commands such as `pytest`_. However,
running these commands does not guarantee that your project is being tested in an isolated
environment, which is the reason why tools like `tox`_ exist.


Use ``pre-commit``
^^^^^^^^^^^^^^^^^^

The style checks take advantage of `pre-commit`_. Developers are not forced but
encouraged to install this tool by running this command:

.. code:: bash

   python -m pip install pre-commit && pre-commit install


Documentation
-------------

To build documentation, you can run the usual rules provided in the
`Sphinx`_ Makefile:

.. code:: bash

   # In Linux environment
   make -C doc/ html && your_browser_name doc/html/index.html

   # In Windows environment
   .\doc\make.bat html && your_browser_name doc/html/index.html

However, the recommended way of checking documentation integrity is to use ``tox``:

.. code:: bash

   tox -e doc && your_browser_name .tox/doc_out/index.html


Distribution
------------

If you would like to create source or wheel files, run these commands to
install the building requirements and then execute the build module:

.. code:: bash

   poetry install --with build
   python -m build
   python -m twine check dist/*


.. LINKS AND REFERENCES
.. _Black: https://github.com/psf/black
.. _Flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _pip: https://pypi.org/project/pip/
.. _pre-commit: https://pre-commit.com/
.. _PyAnsys developer's guide: https://dev.docs.pyansys.com/
.. _pytest: https://docs.pytest.org/en/stable/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _tox: https://tox.wiki/
