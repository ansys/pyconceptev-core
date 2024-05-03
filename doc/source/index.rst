..
   Just reuse the root readme to avoid duplicating the documentation.
   Provide any documentation specific to your online documentation
   here.

.. include:: ../../README.rst


ConceptEV Specific Instructions
-------------------------------

Install the library
^^^^^^^^^^^^^^^^^^^

#. Start by cloning this repository:

.. code:: bash

   git clone https://github.com/ansys-internal/pyconceptev-core

#. Install poetry following your preferred route. See https://python-poetry.org/docs/#installation for example using :code:`pipx`:

.. code:: bash

   pipx install poetry

#. Install dependencies using poetry:

.. code:: bash

   poetry install

#. Activate the poetry environment:

.. code:: bash

   poetry shell

Configure Session using .env file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You need to create a .env file to keep your password and other configurable data.
This file should look something like this:

.. code-block:: bash

   CONCEPTEV_USERNAME = joe.blogs@my_work.com
   CONCEPTEV_PASSWORD = sup3r_s3cr3t_passw0rd
   OCM_URL = https://test.portal.onscale.com/api
   CONCEPTEV_URL = https://dev-conceptev.awsansys3np.onscale.com/api


Get a token
^^^^^^^^^^^

Import the app module and use :code:`get_token`. This should return a random string from the servers to get you access.

.. code-block:: python

   import ansys.conceptev.core.app as pyconceptev

   token = pyconceptev.get_token()


Create a client
^^^^^^^^^^^^^^^

You need to create a client that can access and talk to the API. You can use the health check API to check your connection.

.. code-block:: python

   import ansys.conceptev.core.main as pyconceptev

   with pyconceptev.get_http_client(token, concept_id) as client:
       health = get(client, "/health")
       print(health)


Understand the API
^^^^^^^^^^^^^^^^^^

Use the API documentation at https://dev-conceptev.awsansys3np.onscale.com/api/docs
This shows you which verbs and which routes/paths are available and what inputs/outputs they have.
You can use the verb functions created in this module to make things simpler.

To create a configuration we need to use the verb `post` with route `/configurations` and add the `data` from the schema.

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
