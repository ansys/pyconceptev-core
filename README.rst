PyConceptEV
===========
|pyansys| |python| |MIT|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |python| image:: https://img.shields.io/badge/python-3.9+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python

.. .. |pypi| image:: https://img.shields.io/pypi/v/ansys-conceptev-core.svg?logo=python&logoColor=white
..    :target: https://pypi.org/project/ansys-conceptev-core
..    :alt: PyPI

.. .. |downloads| image:: https://img.shields.io/pypi/dm/ansys-conceptev-core.svg
..    :target: https://pypi.org/project/ansys-conceptev-core/
..    :alt: PyPI Downloads

.. .. |codecov| image:: https://codecov.io/gh/ansys/pyconceptev/graph/badge.svg?token=UZIC7XT5WE
..    :target: https://codecov.io/gh/ansys/pyconceptev
..    :alt: Codecov

.. .. |GH-CI| image:: https://github.com/ansys/pyconceptev/actions/workflows/ci_cd.yml/badge.svg
..    :target: https://github.com/ansys/pyconceptev/actions/workflows/ci_cd.yml
..    :alt: GH-CI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. .. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
..    :target: https://github.com/psf/black
..    :alt: Black

.. .. |pre-commit| image:: https://results.pre-commit.ci/badge/github/ansys/pyconceptev/main.svg
..    :target: https://results.pre-commit.ci/latest/github/ansys/pyconceptev/main
..    :alt: pre-commit.ci


Overview
--------

PyConceptEV is a Python client library for the `Ansys ConceptEV <https://www.ansys.com/products/electronics/ansys-concept-ev>`_
service, which provides a cloud-based design and simulation platform for the concept design
of EV powertrains.

Documentation and issues
------------------------

Documentation for the latest stable release of PyConceptEV is hosted
at `PyConceptEV documentation <https://conceptev.docs.pyansys.com/>`_.

The documentation has these sections:

- `Getting started <https://conceptev.docs.pyansys.com/version/stable/getting_started/index.html>`_: Learn
  how to install PyConceptEV in user mode and quickly begin using it.
- `User guide <https://conceptev.docs.pyansys.com/version/stable/user_guide/index.html>`_: Learn how to
  configure a PyConceptEV session, get a token, and create a client.
- `API reference <conceptev.docs.pyansys.com/version/stable/api/index.html>`_: Understand how the
  `Ansys ConceptEV API documentation <https://conceptev.ansys.com/api/docs>`_ provides for interacting
  programmatically with PyConcept EV.
- `Examples <https://conceptev.docs.pyansys.com/version/stable/examples/index.html>`_: Explore examples
  that show how to use PyConceptEV.
- `Contribute <conceptev.docs.pyansys.com/version/stable/contributing.html>`_: Learn how to
  contribute to the PyConceptEV codebase or documentation.

In the upper right corner of the documentation's title bar, there is an option
for switching from viewing the documentation for the latest stable release
to viewing the documentation for the development version or previously
released versions.

On the `PyConceptEV Issues <https://github.com/ansys/pyconceptev/issues>`_
page, you can create issues to report bugs and request new features. On the
`Discussions <https://discuss.ansys.com/>`_ page on the Ansys Developer portal,
you can post questions, share ideas, and get community feedback.

If you have general questions about the PyAnsys ecosystem, email
`pyansys.core@ansys.com <pyansys.core@ansys.com>`_. If your
question is specific to PyConceptEV, ask your question in an issue
as described in the previous paragraph.

License
-------

PyConceptEV is licensed under the `MIT License <https://github.com/ansys/pyconceptev/blob/main/LICENSE>`_.

PyConceptEV makes no commercial claim over Ansys whatsoever. This library adds a
Python interface for `Ansys ConceptEV <https://www.ansys.com/products/electronics/ansys-concept-ev>`_
without changing the core behavior or license of the original Ansys software.
