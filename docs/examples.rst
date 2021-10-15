========
Examples
========

In order to run these examples you need to create two JSON-files; one for the dataset and one for the actual JSONTas JSON file.

Run the examples by executing

.. code-block:: bash

   jsontas -d dataset.json jsonfile.json

Condition
---------

:obj:`jsontas.data_structures.condition`

Set value in JSON on a condition.
Supported operators are defined here: :obj:`jsontas.data_structures.operator.Operator`

Dataset
^^^^^^^

.. code-block:: json

  {
    "name": "John Doe"
  }

JSON
^^^^

.. code-block:: json

   {
      "occupation": {
         "$condition": {
            "if": {
                "key": "$name",
                "operator": "$eq",
                "value": "John Doe",
            },
            "then": "Engineer",
            "else": "Unemployed"
         }
      }
   }

Result
^^^^^^

.. code-block:: json

   {
      "occupation": "Engineer"
   }



Condition List
--------------

:obj:`jsontas.data_structures.condition`

Set a value in JSON on multiple conditions.
Supported operators are defined here: :obj:`jsontas.data_structures.operator.Operator`

Dataset
^^^^^^^

.. code-block:: json

   {
      "name": "John Doe",
      "occupation": "Engineer"
   }

JSON
^^^^

.. code-block:: json

   {
      "team": {
         "$condition": {
             "if": [
                 {
                     "key": "$name",
                     "operator": "$eq",
                     "value": "John Doe",
                 },
                 {
                     "key": "$occupation",
                     "operator": "$in",
                     "value": ["Engineer", "Manager"]
                 }
             ],
             "then": "The Best Team",
             "else": "The Worst Team"
         }
      }
   }

Result
^^^^^^

.. code-block:: json

   {
      "team": "The Best Team"
   }

Note that condition list is an 'AND' check so all conditions must be True for the 'then' field to execute.

Expand
------

:obj:`jsontas.data_structures.expand`

Expand a value into a list of a certain number of elements.

Dataset
^^^^^^^

.. code-block:: json

   {
      "likes": 2,
      "upvotes": 3
   }

JSON
^^^^

.. code-block:: json

   {
      "upvotes": {
         "$expand": {
            "value": {
               "upvote": true
            },
            "to": "$upvotes"
         }
      },
      "likes": {
         "$expand": {
            "value": "Like",
            "to": "$likes"
         }
      }
   }

Result
^^^^^^

.. code-block:: json

   {
      "upvotes": [
         {"upvote": true},
         {"upvote": true},
         {"upvote": true}
      ],
      "likes": ["Like", "Like"]
   }


Filter
------

:obj:`jsontas.data_structures.filter`

Remove items that do not match a certain filter.
Supported operators are defined here: :obj:`jsontas.data_structures.operator.Operator`

Dataset
^^^^^^^

.. code-block:: json

   {
      "employees": [
         {
            "name": "John Doe",
            "occupation": "Engineer"
         },
         {
            "name": "Jane Doe",
            "occupation": "Engineer"
         },
         {
            "name": "Jane Smith",
            "occupation": "Manager"
         }
      ]
   }

JSON
^^^^

.. code-block:: json

   {
      "engineers": {
         "$filter": {
            "items": "$employees",
            "filters": [
               {
                  "key": "occupation",
                  "operator": "$eq",
                  "value": "Engineer"
               }
            ]
         }
      }
   }

Result
^^^^^^

.. code-block:: json

   {
      "engineers": [
         {
            "name": "John Doe",
            "occupation": "Engineer"
         },
         {
            "name": "Jane Doe",
            "occupation": "Engineer"
         }
      ]
   }



From
----

:obj:`jsontas.data_structures.from_item`

Get a value from a dictionary.

Dataset
^^^^^^^

.. code-block:: json

   {
      "manager": {
         "name": "Jane Smith",
         "occupation": "Manager"
      }
   }

JSON
^^^^

.. code-block:: json

   {
      "manager": {
         "$from": {
            "item": "$manager",
            "get": "name"
         }
      }
   }

Result
^^^^^^

.. code-block:: json

   {
      "manager": "Jane Smith"
   }


List
----

:obj:`jsontas.data_structures.list`

While List is not supposed to be used directly inside a JSON structure one can operate on lists in a dataset like this

Dataset
^^^^^^^

.. code-block:: json

   {
      "employees": [
         {
            "name": "John Doe",
            "occupation": "Engineer"
         },
         {
            "name": "Jane Doe",
            "occupation": "Engineer"
         },
         {
            "name": "Jane Smith",
            "occupation": "Manager"
         }
      ]
   }

JSON
^^^^

.. code-block:: json

   {
      "first_employee": "$employees.0",
      "last_employee": "$employees.-1",
      "first_two_employees": "$employees.:2"
   }

Result
^^^^^^

.. code-block:: json

   {
      "first_employee": {
         "name": "John Doe",
         "occupation": "Engineer"
      },
      "last_employee": {
         "name": "Jane Smith",
         "occupation": "Manager"
      },
      "first_two_employees": [
         {
            "name": "John Doe",
            "occupation": "Engineer"
         },
         {
            "name": "Jane Doe",
            "occupation": "Engineer"
         }
      ]
   }


Operator
--------

:obj:`jsontas.data_structures.operator`

Dataset
^^^^^^^

.. code-block:: json

   {
      "employee": {
         "name": "Jane Doe",
         "occupation": "Engineer"
      }
   }

JSON
^^^^

.. code-block:: json

   {
      "is_manager": {
         "$operator": {
            "key": "$employee.occupation",
            "operator": "$eq",
            "value": "Manager"
         }
      }
   }

Result
^^^^^^

.. code-block:: json

   {
      "is_manager": false
   }


Available operators are further explained in :obj:`jsontas.data_structures.operator`
They are:

* :$eq: :obj:`jsontas.data_structures.operator.Operator._equal`
* :$in: :obj:`jsontas.data_structures.operator.Operator._in`
* :$notin: :obj:`jsontas.data_structures.operator.Operator._notin`
* :$startswith: :obj:`jsontas.data_structures.operator.Operator._startswith`
* :$regex: :obj:`jsontas.data_structures.operator.Operator._regex`


Reduce
------

:obj:`jsontas.data_structures.reduce`

Reduce a list from end to beginning (from right) to a specific value.

Dataset
^^^^^^^

.. code-block:: json

   {
      "max_list_length": 2
   }

JSON
^^^^

.. code-block:: json

   {
      "reduced_list": {
         "$reduce": {
            "list": [
               "element 1",
               "element 2",
               "element 3"
            ],
            "to": "$max_list_length"
         }
      }
   }

Result
^^^^^^

.. code-block:: json

   {
      "reduced_list": [
            "element 1",
            "element 2"
      ]
   }


Request
-------

:obj:`jsontas.data_structures.request`

Make HTTP requests and get JSON values from the response.
Useful for when the dataset is located on a website or if one wants to parse JSON based APIs.

Dataset
^^^^^^^

.. code-block:: json

   {
      "userdata": "https://jsonplaceholder.typicode.com/users/1"
   }

JSON
^^^^

.. code-block:: json

   {
      "user": {
         "$request": {
            "url": "$userdata",
            "method": "GET"
         }
      }
   }

Result
^^^^^^

.. code-block:: json

   {
      "user": {
        "address": {
            "city": "Gwenborough",
            "geo": {
                "lat": "-37.3159",
                "lng": "81.1496"
            },
            "street": "Kulas Light",
            "suite": "Apt. 556",
            "zipcode": "92998-3874"
        },
        "company": {
            "bs": "harness real-time e-markets",
            "catchPhrase": "Multi-layered client-server neural-net",
            "name": "Romaguera-Crona"
        },
        "email": "Sincere@april.biz",
        "id": 1,
        "name": "Leanne Graham",
        "phone": "1-770-736-8031 x56442",
        "username": "Bret",
        "website": "hildegard.org"
      }
   }

Getting a specific response from the response will be further explained below in segment Nested_

Wait
----

:obj:`jsontas.data_structures.wait`

Waiting for a query tree to evaluate to true. A query tree is the full, uresolved, JSON structure that is currently being resolved.
This is mostly used for when utilizing the Request_ datastructure as a way to wait for an API to respond with the data required.

Example will look similar to the Request_ example as this is how the Wait_ structure is normally used.

Dataset
^^^^^^^

.. code-block:: json

   {
      "userdata": "https://jsonplaceholder.typicode.com/users/this_does_not_exist"
   }

JSON
^^^^

.. code-block:: json

   {
      "user": {
         "$wait": {
            "for": {
               "$request": {
                  "url": "$userdata",
                  "method": "GET"
               }
             },
             "interval": 1,
             "timeout": 5,
             "else": "No user found"
         }
      }
   }

Result
^^^^^^

Result will come after 5 seconds.

.. code-block:: json

   {
      "user": "No user found"
   }


Nested
------

Now that we know how all the data structures work in isolation we can start nesting data structures and create more advanced logic.

This example will get the title of all the posts from the user 'Leanne Graham' at https://jsonplaceholder.typicode.com/users

Dataset
^^^^^^^

.. code-block:: json

   {
      "users_api": "https://jsonplaceholder.typicode.com/users",
      "posts_api": "https://jsonplaceholder.typicode.com/posts",
      "username": "Leanne Graham",
      "accepted_status_codes": [200]
   }

JSON
^^^^

.. code-block:: json

   {
      "user_id": {
         "$from": {
            "item": {
               "$filter": {
                  "items": {
                     "$wait": {
                        "for": {
                           "$condition": {
                              "then": {
                                 "$request": {
                                    "url": "$users_api",
                                    "method": "GET"
                                 }
                              },
                              "if": {
                                 "key": "$response.status_code",
                                 "operator": "$in",
                                 "value": "$accepted_status_codes"
                              },
                              "else": null
                           }
                        },
                        "interval": 1,
                        "timeout": 20,
                        "else": {}
                     }
                  },
                  "filters": [
                     {
                        "key": "name",
                        "operator": "$eq",
                        "value": "$username"
                     }
                  ]
               }
            },
            "get": "id"
         }
      },
      "posts": {
         "$from": {
            "item": {
               "$request": {
                  "url": "$posts_api",
                  "method": "GET",
                  "params": {
                     "userId": "$this.user_id.0"
                  }
               }
            },
            "get": "title"
         }
      }
   }

Result
^^^^^^

.. code-block:: json

   {
      "posts": [
         "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
         "qui est esse",
         "ea molestias quasi exercitationem repellat qui ipsa sit aut",
         "eum et est occaecati",
         "nesciunt quas odio",
         "dolorem eum magni eos aperiam quia",
         "magnam facilis autem",
         "dolorem dolore est ipsam",
         "nesciunt iure omnis dolorem tempora et accusantium",
         "optio molestias id quia eum"
      ],
      "user_id": [
          1
      ]
   }


Conclusion
----------

There are many crazy ways of utilizing JSONTas and it's quite impossible to write examples for each and every use-case.
If there are any questions then please to not hestitate contacting the maintainers or writing an issue in github.
We encurage you to play around with it and send a PR with new examples.
