=======
JSONTas
=======

JSONTas is a tool for generating dynamic JSON data.

Description
===========

JSONTas adds conditionals and logic to JSON files in order to create dynamic JSON data depending on which dataset you supply.

It opens up the possibility to create generic tools where most of the operations are done by executing JSONTas on the data.

Documentation: https://jsontas.readthedocs.io/en/latest


Features
========

- Simple yet powerful syntax.
- HTTP requests on parse
- Separation of environments by providing different datasets.

Installation
============

Install the project by running:

   pip install jsontas

Examples
========

First we create two datasets. One for our 'dev' environment and one for our 'prod' environment.

Dataset 'dev.json'
------------------

.. code-block:: JSON

   {
      "mode": "dev",
      "database": "dev_db"
   }


Dataset 'prod.json'
-------------------

.. code-block:: JSON

   {
      "mode": "prod",
      "database": "prod_db"
   }

JSONTas JSON file
-----------------

Next up, let's create our JSONTas file.

.. code-block:: JSON

   {
      "database": {
         "host": "myawesomedb.example.com",
         "database": "$database"
      },
      "message": {
         "$condition": {
            "if": {
               "key": "$mode",
               "operator": "$eq",
               "value": "dev"
            },
            "then": "This is the DEV server.",
            "else": "This is the PROD server."
         }
      }
   }

JSONTas execute with 'dev' dataset
----------------------------------

.. code-block:: bash

   jsontas -d dev.json data.json

.. code-block:: JSON

   {
      "database": {
         "host": "myawesomedb.example.com",
         "database": "dev_db"
      },
      "message": "This is the DEV server."
   }

JSONTas execute with 'prod' dataset
-----------------------------------

.. code-block:: bash

   jsontas -d prod.json data.json

.. code-block:: JSON

   {
      "database": {
         "host": "myawesomedb.example.com",
         "database": "prod_db"
      },
      "message": "This is the PROD server."
   }

These examples only show the bare minimum.
For more examples look at our documentation at: https://jsontas.readthedocs.io/en/latest

Contribute
==========

- Issue Tracker: https://github.com/AxisCommunications/jsontas/issues
- Source Code: https://github.com/AxisCommunications/jsontas

Support
=======

If you are having issues, please let us know.
Email tobias.persson@axis.com or just write an issue.
