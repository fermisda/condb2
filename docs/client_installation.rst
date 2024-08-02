ConDB2 Client Installation
=========================

There are 2 ways to install the ConDB2 client.

PyPi isntallation
-----------------

    .. code-block:: shell

        $ pip install fnal.wda-condb2


Installation from github
------------------------

    .. code-block:: shell

        $ git clone https://github.com/fermisda/condb2.git
        $ cd condb2
        $ pip install .


Once the client is installed, ConDB2 library module will be available as ``condb2``:

    .. code-block:: python

        from condb2 import ConDB, ConDBClient
        ...

