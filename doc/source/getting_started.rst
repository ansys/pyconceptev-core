.. _ref_getting_started:

Getting started
###############

This section describes how to install PyConceptEV in user mode and
quickly begin using it. If you are interested in contributing to PyConceptEV,
see :ref:`contribute` for information on installing in developer mode.


Installation
^^^^^^^^^^^^

Before installing PyConceptEV, make sure that you have the latest version
of `pip <https://pypi.org/project/pip/>`_ by running this command:

.. code:: bash

   python -m pip install -U pip

Then, install PyConceptEV with this command:

.. code:: bash

   python -m pip pip install ansys-conceptev-core


Install the library
^^^^^^^^^^^^^^^^^^^

#. Clone the repository:

   .. code:: bash

      git clone https://github.com/ansys-internal/pyconceptev-core

#. Install Poetry using one of the `installation options <https://python-poetry.org/docs/#installation>`_
   described in the Poetry documentation.

   For example, to install with ``pipx``, run this command:

   .. code:: bash

      pipx install poetry

#. Install dependencies using Poetry:

   .. code:: bash

      poetry install

#. Activate the Poetry environment:

   .. code:: bash

      poetry shell

