#install_twisted_rector must be called before importing the reactor

import getpass
import platform, subprocess
from threading import Thread
import os
import datetime
import sys
import sys
import time
import logging

from functools import partial

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
from kivy.animation import Animation

# A simple kivy App, with a textbox to enter messages, and
# a large label to display all the messages received from
# the server
class TwistedClientApp(App):
	connection = None
	user_os = None
	user = None
	labelmsg = ""
	chat_online_details = ""
	haha = []
	y=0
	notify_events = []
	available_users = []
	def build(self):
		root = self.pro_info()
        #self.connect_to_server()
		self.start_thread()
		return root
	def pro_info(self):
		self.layout = FloatLayout(size=(800,800))
		self.Mainlabel = Label(text="SharePy",color=(0.6,0.7,0.2,1),font_size="65sp",pos=(280,450),size_hint=(.3,.3))
		self.layout.add_widget(self.Mainlabel)
		self.cont_but = Button(text="Cont...",background_color=(0.2,0.3,0.88,1),pos=(700,30),size_hint=(.12,.1))
		self.layout.add_widget(self.cont_but)
		self.INFO = Label(size_hint=(.3,.3),pos=(230,300),color=(0.6,0.3,0.1,1),font_size="21dp")
		self.INFO2 = Label(size_hint=(.3,.3),pos=(230,150),color=(0.3,0.3,0.7,1),font_size="21dp")
		self.INFO.text = "SharePy is a project based on File Sharing.\nIts a project developed in Kivy using Python.\n\nBasic Features include:\n "
		self.INFO2.text = self.INFO2.text + "\n-> Zero Configuration\n-> File Transfering\n-> File Syncing\n-> File Searching\n-> Notification Broadcasting on File Events\n-> ChatBot for communication between Clients\n-> File Listing"
		self.INFO3 = Label(text="Members:\nVarun Malhotra\nMayank Bhola\nHarsh Bhatia",color=(0.7,0.1,0.1,1),pos=(150,40),size_hint=(0.2,0.2),font_size="21dp")
		
		self.layout.add_widget(self.INFO)
		self.layout.add_widget(self.INFO2)
		self.layout.add_widget(self.INFO3)
		self.anim_info2 = Animation(x=80,y=150, opacity=0.4, d=0.4,t ='in_quad') +\
			Animation(x=230,y=150, opacity=1, d=0.5)
		self.anim_info2.start(self.INFO2)
		self.anim_info3 = Animation(x=80,y=20, opacity=0.4, d=0.6,t ='in_quad') +\
			Animation(x=150,y=20, opacity=1, d=0.8)
		self.anim_info3.start(self.INFO3)
		self.cont_but.bind(on_press=self.setup_gui)
		
		return self.layout
	def setup_gui(self,object):
		global user 
		user = getpass.getuser()
		global user_os 
		user_os = platform.system()
		
		self.Mainlabel = Label(text="SharePy",color=(0.6,0.7,0.2,1),font_size="65sp",pos=(280,450),size_hint=(.3,.3))
		
		self.label = TextInput(hint_text='Connecting...\n',size_hint=(.68,.5),pos=(20,120),readonly=True,focus=True)
		self.dir_loc = TextInput(hint_text='Your root directory is: ',size_hint=(.68,.07),pos=(20,430),readonly=True,background_color=(192,192,192,0.3),foreground_color=(255,255,255,1))
		self.button =Button(text="Start Client",size_hint=(.2,.2),background_color=(0.7,0.2,0.3,1),pos=(50,100))
	
		self.ctexthost = TextInput(text="localhost",hint_text="Enter host",size_hint=(.2,.1),pos=(-150,350),multiline=False,background_color=(0.4,0.5,1,0.9),foreground_color=(255,255,255,1))
		self.ctextport = TextInput(text="8000",hint_text="Enter port",size_hint=(.2,.1),pos=(-150,250),multiline=False,background_color=(0.4,0.5,1,.9),foreground_color=(255,255,255,1))

		self.button1 = ToggleButton(text="Search a File",size_hint=(.2,.2),pos=(10,500),group="file_share",font_size='18sp')
		self.button2 = ToggleButton(text="Get a File",size_hint=(.2,.2),pos=(210,500),group="file_share",font_size="18sp")
		self.button3 = Button(text="Search a File",size_hint=(.17,.15),pos=(20,520),background_color=(0.5,0.7,1,1),font_size="18sp")
		self.button4 = Button(text="List Directory",size_hint=(.17,.15),pos=(150,520),background_color=(0.4,1,0.3,1),font_size="18sp")
		self.button4.bind(on_press=self.opentextinput)
		
		self.closeclient = Button(text="Close Client",pos=(425,520),size_hint=(0.17,0.15),background_color=(0.8,0.3,0.1,1),font_size="18sp")
		self.closeclient.bind(on_press=self.CloseClient)
		
		self.notify_ground = TextInput(text="I notify events",pos=(600,0),background_color=(0.7,0.5,0.9,1),size_hint=(.3,1),readonly=True,scroll_y=10)
		self.chat_ground = TextInput(text="CHAT BOX",pos=(600,0),background_color=(0.7,0.5,0.9,1),size_hint=(.3,1),readonly=True,scroll_y=10)
		
		self.chatbox = Button(text="Chat Box",pos=(563,520),size_hint=(0.17,0.15),background_color=(0.3,0.3,0.7,1),font_size="18sp")
		self.chatbox.bind(on_press=self.chathistory)
		
		self.reponame = TextInput(text="Hellosnp",hint_text="Enter RepoName",pos=(200,300),size_hint=(0.5,0.1),multiline=False,focus=True)
		
		self.button.bind(on_press=self.connect_to_server)
		self.label_info = TextInput(text="Hi i'm a alebe;",pos=(0,610),background_color=(0.7,0,0,1),size_hint=(1,.2),readonly=True)
		self.notify_but = Button(text="Recent events",size_hint=(.17,.15),pos=(290,520),background_color=(0.8,0.2,0.3,1),font_size="18sp")
		self.notify_but.bind(on_press=self.recent_act)
		
		self.cancel_event = Button(text="Close",size_hint=(0.27,0.06),pos=(600,0),background_color=(255,0,0,0.6))
		self.cancel_chat = Button(text="Close",size_hint=(0.27,0.06),pos=(600,0),background_color=(255,0,0,0.6))
		self.repolabel = Label(text="Create your own Repository/New Folder by providing the name below",pos=(210,320),size_hint=(0.5,0.5),color=(0.6,0.3,0.1,1),font_size="20dp")
		#self.layout = FloatLayout(size=(800,800))
		
		self.update = Button(text="Update",background_color=(0.3,0.3,0.9,1),size_hint=(.25,.1),pos=(600,550))
		
		self.setup_load()
		
		
		return self.layout
	def setup_load(self):
		
		self.layout.clear_widgets()
		self.layout.add_widget(self.button)
		self.layout.add_widget(self.Mainlabel)
		self.layout.add_widget(self.ctexthost)
		self.layout.add_widget(self.ctextport)
		
		self.anim_host = Animation(x=280,y=550, opacity=0.4, d=0.2,t ='in_quad') +\
			Animation(x=280,y=450, opacity=1, d=0.2)
		self.anim_host.start(self.Mainlabel)
		
		self.anim_host = Animation(x=0,y=350, opacity=0.4, d=0.5,t ='in_quad') +\
			Animation(x=50,y=350, opacity=1, d=0.6)
		self.anim_host.start(self.ctexthost)
		
		self.anim_port = Animation(x=0,y=250, opacity=0.4, d=0.5,t ='in_quad') +\
			Animation(x=50,y=250, opacity=1, d=0.6)
		self.anim_port.start(self.ctextport)
		
		self.anim_startbut = Animation(x=0,y=100, opacity=0.4, d=0.5,t ='in_quad') +\
			Animation(x=50,y=100, opacity=1, d=0.6)
		self.anim_startbut.start(self.button)
	def setup_utilities(self):
		self.layout.clear_widgets()
		#self.repolabel = Label(text="Create your own Repository/New Folder by providing the name below",pos=(200,500))
		#self.repolabel.text = "Create your own Repository/New Folder by providing the name below"
		self.layout.add_widget(self.repolabel)
		self.layout.add_widget(self.reponame)
		self.reponame.bind(on_text_validate=self.start_utilities)
		return self.layout
	def start_utilities(self, *args):
			root_dirname = self.reponame.text
			if not os.path.exists(root_dirname):
				os.makedirs(root_dirname)
				#output = subprocess.Popen(["git","init"],shell=True,stdout=subprocess.PIPE).communicate()[0]
			os.chdir(root_dirname)
			self.dir_loc.text = os.getcwd()
			self.layout.clear_widgets()
			self.layout.add_widget(self.button3)
			self.layout.add_widget(self.button4)
			self.layout.add_widget(self.closeclient)
			self.layout.add_widget(self.notify_but)
			self.layout.add_widget(self.chatbox)
			self.layout.add_widget(self.label)
			self.layout.add_widget(self.dir_loc)
			self.layout.add_widget(self.label_info)
			
			self.anim_host = Animation(x=20,y=520, opacity=0.4, d=0.5,t ='in_quad') +\
				Animation(x=20,y=480, opacity=1, d=0.6)
			self.anim_host.start(self.button3)
		
			self.anim_port = Animation(x=155,y=520, opacity=0.1, d=0.5,t ='in_quad') +\
				Animation(x=155,y=480, opacity=1, d=0.6)
			self.anim_port.start(self.button4)
		
			self.anim_button = Animation(x=290,y=520, opacity=0.1, d=0.5,t ='in_quad') +\
				Animation(x=290,y=480, opacity=1, d=0.6)
			self.anim_button.start(self.notify_but)
			
			self.anim_close = Animation(x=425,y=520, opacity=0.1, d=0.5,t ='in_quad') +\
				Animation(x=425,y=480, opacity=1, d=0.6)
			self.anim_close.start(self.closeclient)
			
			self.anim_chat = Animation(x=563,y=520, opacity=0.1, d=0.5,t ='in_quad') +\
				Animation(x=563,y=480, opacity=1, d=0.6)
			self.anim_chat.start(self.chatbox)
			
			return self.layout
	def connect_to_server(self,*args):
	
		if((self.ctextport.text).isdigit()):
			self.conn = reactor.connectTCP(str(self.ctexthost.text), int(self.ctextport.text), EchoFactory(self))
			#client_info = "0$#" + 
			#self.connection.write()
			self.label.text = "Connecting...\n"
		else:
			
			self.label.text  = "Not Connected...\nPlease enter valid port" 	
	def on_connection(self, connection):
		self.print_message("Connected Succesfully!")
		self.connection = connection
		self.setup_utilities()

	def send_message(self,connection):
		msg = self.textbox.text
		if msg and self.connection:
			msg = "2$#" + user + "@" + user_os + ": " + msg
			self.connection.write(str(msg))
			self.textbox.text = ""

	def print_message(self, msg):
		copr = msg.split("$#")[0]
		
		#print msg
		if copr.isdigit():
			if (int(copr)==2):
				self.label.text = msg.split("$#")[1] + "\n"
				#print msg.split("$#")[1]
			elif (int(copr)==8):
				self.sendarea.text = self.sendarea.text + msg.split("8$#")[1] + "\n"
				print "recveived msg - " + (msg.split("8$#")[1]).split("##")[1] + " from ip add" + (msg.split("8$#")[1]).split("##")[0]
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
				#self.popup = Popup(title='Notification      Click outside to exit',content=Label(text=str(msg)),size_hint=(.8, .4))
				#self.popup.open()
				self.layout.remove_widget(self.label_info)
				self.layout.add_widget(self.label_info)
				self.label_info.text = str(msg)
				self.anim = Animation(x=0,y=550, opacity=0, d=1, t='in_back') +\
					Animation(x=0,y=480, d=1, opacity=0.8) +\
					Animation(x=0,y=480, d=4,opacity=1) +\
					Animation(x=0,y=650, opacity=0, d=2)
				self.anim.start(self.label_info)
				self.notify_events.append(str(msg))
				#call function recent_act
			elif (int(copr)==5):
				msg = msg.split("$#")[1]
				#self.available_users.append(str(msg))
				msg = msg.split(',')
				self.chat_ground.text = " "
				self.haha =  [0]*30
				self.y = 0
				#print len(msg)
				for on in range (0,len(msg)-1):
					self.haha[on] = Button(text=str(msg[on]),background_color=(0,1,0,1),pos=(600,515-self.y),size_hint=(0.25,0.07))
					self.layout.add_widget(self.haha[on])
					self.haha[on].bind(on_press= partial(self.open_chat_for,msg[on]))
					self.y=self.y+45
				self.layout.add_widget(self.update)	
			return self.layout	
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

	def CloseClient(self, *args):
		self.conn.disconnect()
		self.layout.clear_widgets()
		#os.chdir(cd..)
		self.setup_load()
		path = os.path.dirname(os.getcwd())
		os.chdir(path)
		#output = subprocess.Popen(["cd.."],stdout=subprocess.PIPE).communicate()[0]
		print os.getcwd()
		return self.layout
		
	def chathistory(self, *args):
		self.layout.remove_widget(self.chatbox)
		self.layout.clear_widgets()
		
		
		self.sendarea = Label(text=" ",size_hint=(.2,.2),pos=(80,400),font_size="19dp",color=(0.7,0.5,0.6,1))
		self.layout.add_widget(self.sendarea)
		
		self.update.bind(on_press=self.cancel_chat_box)
		self.layout.add_widget(self.chat_ground)
		self.backbutton = Button(text="Back <-",background_color=(1,0.1,0.1,1),size_hint=(.11,.1),pos=(30,500),font_size="20dp")
		self.layout.add_widget(self.backbutton)
		self.backbutton.bind(on_press=self.start_utilities)
		#self.layout.add_widget(self.cancel_chat)
		#self.cancel_chat.bind(on_press=self.cancel_chat_box)
		self.chat_online_details = "5$#" + user + "@" + user_os + ": " + "Ready to chat"
		#print self.chat_online_details
		self.connection.write(str(self.chat_online_details))
		#return self.layout

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

	def recent_act(self, textevent):
		self.layout.remove_widget(self.notify_but)
		self.layout.add_widget(self.notify_ground)
		self.anim_ground = Animation(x=700,y=0, opacity=0.3, d=0.2,t ='in_quad') +\
			Animation(x=600,y=0, opacity=1, d=0.2)
		self.anim_ground.start(self.notify_ground)
		
		
		self.layout.add_widget(self.cancel_event)
		self.cancel_event.bind(on_press=self.cancel_event_window)
		self.notify_ground.text = ""
		for l in self.notify_events:
			self.notify_ground.text = self.notify_ground.text + str(l) + '\n'
		return self.layout
	def cancel_event_window(self,*args):
		self.layout.remove_widget(self.notify_ground)
		self.layout.remove_widget(self.cancel_event)
		self.layout.add_widget(self.notify_but)
		return self.layout
		
	def cancel_chat_box(self,args):
		
		self.layout.clear_widgets()
		self.chathistory()
		return self.layout
		
	def open_chat_for(self,ipadd,args):
		self.chat_lid = TextInput(hint_text="Send msg",pos=(100,50),size_hint=(.6,.1),multiline=False,focus=True)
		self.layout.add_widget(self.chat_lid)
		self.chat_lid.bind(on_text_validate=partial(self.send_to_ip,ipadd))
	def send_to_ip(self,ipadd,args):	
		
		print "send msg - '" + self.chat_lid.text +"' to ip address - "+ipadd
		self.connection.write("8$#"+str(ipadd)+"##"+str(self.chat_lid.text))
		self.chat_lid.text = ""
		self.chat_lid.focus = True
		
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
		if ( self.getext(event.src_path) == ".txt" or self.getext(event.src_path) == ".py"):
			print "e=",event
			global textevent
			textevent = event
			#self.obj = TwistedClientApp()
			self.obj.notify(textevent)
	def getext(self,filename):
		return os.path.splitext(filename)[-1].lower()

class SendMessage(protocol.Protocol):
	def __init__(self,obj):
		self.obj = obj
		self.transport.write("8$#Client.py")
		
if __name__ == '__main__':
	t =  TwistedClientApp()
	t.run()
	