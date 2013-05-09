SharePy Tutorial
================

1. Install Kivy from `Installation guides for Kivy <http://kivy.org/docs/installation/installation.html/>`_

2. Clone this project and copy paste the SharePy folder and change to this directory . If you are on linux platform simply write **python server.py** & **python client.py** in different terminals. For windows, open kivy.bat and run both the files in order as mentioned above.

3. In server app, give the port number to start server at desired port and sstart the app by clicking the start button.

4. Now in client app, give the I.P. address for the host machine (localhost/127.0.0.1 for same PC) and same port as was given in server app. Simply start the client app too and the server app will add the connected clients and display them.

5. Now a folder named Hellosnp (can be changed later) will automatically be created in current directory which will act as a client's local repo. Each client has its own.

6. Client can search for available files on server.

7. Folder *Hellosnp* will be under watch all the time for any file related events i.e filedelete event, file modifiedevent, filecreate event and so on for each client.
It is achieved using a python module **watchdog**. You can grab this at `Watchdog <https://github.com/gorakhargosh/watchdog/>`_

8. Any file event will broadcast the notification to all the clients informing the event and its cause.

9. Still deveoping...

Warning::

   Run server and client on same platform
   Cross-platform connection and features will be availbale soon


