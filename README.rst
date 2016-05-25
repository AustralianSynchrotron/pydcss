Usage
=====

DCSS client
-----------

.. code-block:: python

    >>> dcss_host = '10.11.12.13'
    >>> session_id = '<session id from users.txt>'
    >>> client = dcss.Client(dcss_host, session_id)
    >>> client.run_operation('some_operation')


DHS
---

.. code-block:: python

    import dcss

    class MyDHS(dcss.Server):
        def some_dhs_operation(self, operation, *args):
            try:
                do_things()
            except Exception as error:
                operation.operation_error(str(error))
            else:
                operation.operation_completed('things were done')

    my_dhs = MyDHS('my_dhs', '10.11.12.13')
    my_dhs.loop()
