.. _ref_api_ref:

API reference
#############

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

