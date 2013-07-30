MinorProject
============
PyShare
-------

It's a file sharing app which can be used for a collaborative project management.
It uses Python-Kivy framework as its User interface. Since Kivy is cross-platform, this app runs all platforms.

Based on Twisted Server-Clietn Model, this app helps team members to collaborate their work simultaneoulsy with others.
http://twistedmatrix.com/documents/12.2.0/core/examples/

Basic file transmission, searching and accessing among the members.
A Repository is automatically generated on client's machine which is under watch for any file operation. 
Any such event triggers the notification to be braodcasted to all the client's.
This helps everyone working if, on same project, to know the status and work of others.
Python module Watchdog helps in triggering pop-ups upon any file event.
https://github.com/gorakhargosh/watchdog

Requirements
------------

Installing from PyPI using pip:

.. code-block:: bash

    pip install watchdog

Installing from PyPI using easy_install:

.. code-block:: bash

    easy_install watchdog

Running the App
---------------

1. cd PyShare
2. run python server.py and enter the port to start the server 
3. run python client.py on different machines and enter same port and host address to access the utilities.


