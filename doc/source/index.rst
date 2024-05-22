..
   Just reuse the root readme to avoid duplicating the documentation.
   Provide any documentation specific to your online documentation
   here.

.. include:: ../../README.rst


PyConceptEV usage
-----------------

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

Configure a session using an ``ENV`` file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You must create an ``ENV`` file to keep your password and other configurable data in.
The file should look like this:

.. code-block:: bash

   CONCEPTEV_USERNAME = joe.blogs@my_work.com
   CONCEPTEV_PASSWORD = sup3r_s3cr3t_passw0rd
   OCM_URL = https://prod.portal.onscale.com/api
   CONCEPTEV_URL = https://conceptev.ansys.com/api


Get a token
^^^^^^^^^^^

Import the main module and use the :code:`get_token()` method to get a
a random access string from the server.

.. code-block:: python

   import ansys.conceptev.core.main as pyconceptev

   token = pyconceptev.get_token()


Create a client
^^^^^^^^^^^^^^^

You must create a client that can access and talk to the Ansys ConceptEV API. You can use
the health check endpoint to check your connection.

.. code-block:: python

   import ansys.conceptev.core.main as pyconceptev

   with pyconceptev.get_http_client(token, concept_id) as client:
       health = get(client, "/health")
       print(health)


Understand the API
^^^^^^^^^^^^^^^^^^

The `Ansys ConceptEV API documentation <https://conceptev.ansys.com/api/docs>`_
shows you which verbs and which routes or paths are available and what inputs
and outputs they have. You can use the verb functions in this API to make
things simpler.

To create a configuration, you must use the verb ``POST`` with the route ``/configurations``
and add the ``data`` object from the schema:

.. code-block:: python

   data = {
       "name": "New Aero Config",
       "drag_coefficient": 1,
       "cross_sectional_area": 2,
       "config_type": "aero",
   }
   pyconcetpev.post(client, "/configurations", data=data)

.. toctree::
   :hidden:
   :maxdepth: 3

   changelog
