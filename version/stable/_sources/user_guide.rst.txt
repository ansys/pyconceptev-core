.. _ref_user_guide:

User guide
##########

This section explains how to use PyConceptEV.

Configure a session using an ``ENV`` file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create an ``ENV`` file to keep your password and other configurable data in.
The file should look like this:

.. code-block:: bash

   CONCEPTEV_USERNAME = joe.blogs@my_work.com
   CONCEPTEV_PASSWORD = sup3r_s3cr3t_passw0rd
   OCM_URL = https://prod.portal.onscale.com/api
   CONCEPTEV_URL = https://conceptev.ansys.com/api


Get a token
^^^^^^^^^^^

Import the PyConceptEV core module and use the :code:`get_token()` method to get a
a random access string from the server.

.. code-block:: python

   import ansys.conceptev.core.main as pyconceptev

   token = pyconceptev.get_token()


Create a client
^^^^^^^^^^^^^^^

Create a client that can access and talk to the Ansys ConceptEV API. You can use
the health check endpoint to check your connection.

.. code-block:: python

   import ansys.conceptev.core.main as pyconceptev

   with pyconceptev.get_http_client(token, concept_id) as client:
       health = get(client, "/health")
       print(health)

