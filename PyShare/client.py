#install_twisted_rector must be called before importing the reactor

import getpass
import platform
from threading import Thread
import os
import datetime
import sys
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

from kivy.support import install_twisted_reactor
install_twisted_reactor()


#A simple Client that send messages to the echo server
from twisted.internet import reactor, protocol

textevent = ""



class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        self.factory.app.print_message(data)

class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient
    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        self.app.print_message("connection lost")

    def clientConnectionFailed(self, conn, reason):
        self.app.print_message("connection failed")


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup

# A simple kivy App, with a textbox to enter messages, and
# a large label to display all the messages received from
# the server
class TwistedClientApp(App):
	connection = None
	user_os = None
	user = None
	labelmsg = ""
	def build(self):
		root = self.setup_gui()
        #self.connect_to_server()
		self.start_thread()
		return root
	
	def setup_gui(self):
        #self.textbox = TextInput(size_hint_y=.1, multiline=False)
        #self.textbox.bind(on_text_validate=self.send_message)
		
		self.label = TextInput(hint_text='Connecting...\n',size_hint=(.6,.5),pos=(280,120),readonly=True,focus=True)
		self.dir_loc = TextInput(hint_text='Your root directory is: ',size_hint=(.6,.07),pos=(150,430),readonly=True,background_color=(192,192,192,0.3),foreground_color=(255,255,255,1))
		self.button =Button(text="Start Client",size_hint=(.2,.2),pos=(50,100))
	
		self.ctexthost = TextInput(hint_text="Enter host",size_hint=(.2,.1),pos=(50,350),multiline=False,background_color=(0,0,255,0.3),foreground_color=(255,255,255,1))
		self.ctextport = TextInput(hint_text="Enter port",size_hint=(.2,.1),pos=(50,250),multiline=False,background_color=(0,0,255,.3),foreground_color=(255,255,255,1))

		self.button1 = ToggleButton(text="Search a File",size_hint=(.2,.2),pos=(10,500),group="file_share",font_size='18sp')
		self.button2 = ToggleButton(text="Get a File",size_hint=(.2,.2),pos=(210,500),group="file_share",font_size="18sp")
		self.button3 = Button(text="Search a File",size_hint=(.2,.2),pos=(150,480),background_color=(0,255,255,0.7),font_size="18sp")
		self.button4 = Button(text="List Directory",size_hint=(.2,.2),pos=(470,480),background_color=(0,255,0,0.5),font_size="18sp")
		self.button4.bind(on_press=self.opentextinput)
		
		self.button.bind(on_press=self.connect_to_server)	
		self.layout = FloatLayout(size=(600,600))
		
		self.layout.add_widget(self.label)
		self.layout.add_widget(self.dir_loc)
		self.layout.add_widget(self.button)
		#self.layout.add_widget(self.button1)
		#self.layout.add_widget(self.button2)
		self.layout.add_widget(self.button3)
		self.layout.add_widget(self.button4)
		self.layout.add_widget(self.ctexthost)
		self.layout.add_widget(self.ctextport)
		global user 
		user = getpass.getuser()
		global user_os 
		user_os = platform.system()
		root_dirname = "Hellosnp"
		if not os.path.exists(root_dirname):
			os.makedirs(root_dirname)
		os.chdir(root_dirname)
		
		self.dir_loc.text = os.getcwd()
		return self.layout

	def connect_to_server(self,*args):
	
		if((self.ctextport.text).isdigit()):
			reactor.connectTCP(str(self.ctexthost.text), int(self.ctextport.text), EchoFactory(self))
			#client_info = "0$#" + 
			#self.connection.write()
			self.label.text = "Connecting...\n"
		else:
			
			self.label.text  = "Connecting...\nPlease enter valid port" 	
	def on_connection(self, connection):
		self.print_message("connected succesfully!")
		self.connection = connection

	def send_message(self,connection):
		msg = self.textbox.text
		if msg and self.connection:
			msg = "2$#" + user + "@" + user_os + ": " + msg
			self.connection.write(str(msg))
			self.textbox.text = ""

	def print_message(self, msg):
		copr = msg.split("$#")[0]
		print msg
		if copr.isdigit():
			if (int(copr)==2):
				self.label.text = msg.split("$#")[1] + "\n"
				print msg.split("$#")[1]
			elif (int(copr)==4):
				msg = msg.split("$#")[1]
				g = msg.split(": <")[1]
				o = g.split(": ")[0]
				if o=="FileMovedEvent":
					d = g.split(": src_path=")[1]
					e = d.split(", ")[0]
					f = d.split(", ")[1]
					f1 = f.split(">")[0]
					msg = "A file at\n" + e + "\nis moved to\n" + f1
				else:
					of = g.split(": ")[1]
					print o
					f = g.split("src_path=")[1]
					f1 = f.split(">")[0]
					msg = "A file at\n" + f1 + "\n is " + o
				self.popup = Popup(title='Notification      Click outside to exit',content=Label(text=str(msg)),size_hint=(.8, .4))
				self.popup.open()
		else:
			self.label.text = msg + "\n"
	def opentextinput(self, *args):
		self.textbox = TextInput(size_hint=(.9,.1),pos=(0,0), multiline=False,focus=True)
		self.textbox.bind(on_text_validate=self.send_message)	
		self.closebutton = Button(text="Close",size_hint=(.1,.1),pos=(720,0),background_color=(255,0,0,1))
		self.closebutton.bind(on_press=self.destroy)
		self.layout.add_widget(self.textbox)
		self.layout.add_widget(self.closebutton)

	def destroy(self, *args):
		self.layout.remove_widget(self.closebutton)
		self.layout.remove_widget(self.textbox)	

	def background_stuff(self):	
		while True:
			#self.logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
			self.path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
			self.event_handler = ChangeHandler(self)
			self.observer = Observer()
			self.observer.schedule(self.event_handler, self.path, recursive=True)
			self.observer.start()
			try:
				while True:
					time.sleep(1)
			except KeyboardInterrupt:
				self.observer.stop()
				self.observer.join()

	def start_thread(self):
		t = Thread(target=self.background_stuff)
		t.start()
	
	def notify(self,textevent):
		textevent1 = "4$#" + user + "@" + user_os + ": " + str(textevent)
		#textevent = "4$#" + textevent
		self.connection.write(str(textevent1))

		return self.layout
	def dismiss_popup(instance):
		return False
class ChangeHandler(FileSystemEventHandler):
	def __init__(self,obj):
		self.obj = obj
	def on_any_event(self,event):
		if event.is_directory:
			#print "A folder is added"
			print "e=",event
			global textevent
			textevent = event 
			self.obj.notify(textevent)
		if self.getext(event.src_path) == ".txt":
			print "e=",event
			global textevent
			textevent = event
			#self.obj = TwistedClientApp()
			self.obj.notify(textevent)
	def getext(self,filename):
		return os.path.splitext(filename)[-1].lower()

if __name__ == '__main__':
	t =  TwistedClientApp()
	t.run()
	