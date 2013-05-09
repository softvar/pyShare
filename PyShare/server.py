# install_twisted_rector must be called before importing  and using the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()


from twisted.internet import reactor
from twisted.internet import protocol

clients = []

class EchoProtocol(protocol.Protocol):
    def connectionMade( self ):
        self.factory.numProtocols = self.factory.numProtocols+1
        print "Connection from",self.transport.getPeer()
        self.temp = str(self.transport.getPeer())
        self.client_info = self.temp.split(", ")[1]
        self.client_info = self.client_info.split("'")[1]
        self.factory.addClient( self,self.client_info )
		
    def connectionLost( self , reason ):
        self.factory.numProtocols = self.factory.numProtocols-1
        self.temp = str(self.transport.getPeer())
        self.client_info = self.temp.split(", ")[1]
        self.client_info = self.client_info.split("'")[1]
        self.factory.delClient( self,self.client_info )

    def dataReceived(self, data):
        proc = data.split("$#")[0]
        if (int(proc)==2):
            response = self.factory.app.handle_message(data)
            if response:
			    self.transport.write(response)
        elif (int(proc)==4):
            response = self.factory.sendAll(self.factory.app.handle_message(data))
        elif (int(proc)==5):
            response = self.factory.app.handle_message(data)
            if response:
                self.transport.write(response)			
        elif (int(proc)==8):
            response = self.factory.sendTo(self,data)
        
class EchoFactory(protocol.Factory):
    protocol = EchoProtocol
    numProtocols = 0
    clients = []
    clientss = []
    
    def __init__(self, app):
        self.app = app
        #self.obj = obj
    def addClient(self, obj,newclient):
        self.clients.append( newclient )
        self.clientss.append(obj)
        #print self.clientss
        self.app.client_conn(self.clients)
    def delClient(self, obj,client):
        self.clients.remove( client )
        self.clientss.remove(obj)
        #print self.clientss
        self.app.client_conn(self.clients)
    def sendAll(self, message):
        #print self.clients
        for proto in self.clientss:
                proto.transport.write( message )
    def sendTo(self,obj,data):
        i = j = 0
        pos = 0
        print data
        data = data.replace(" ","")
        d1 = data.split("8$#")[1]
        print d1
        d2 = d1.split("##")[0]
        print d2
        forward_msg_to = []
        d3 = d1.split("##")[1]
        for scan_ip in self.clients:
            print scan_ip
            if (d2==scan_ip):
                pos = i
            i = i + 1
        print pos
        for search in self.clientss:
            if (j==pos):
                forward_msg_to.append(search)
            j = j + 1
        print search
        for send_to in forward_msg_to:
            send_to.transport.write(data)
		


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import subprocess
import os, platform

class TwistedServerApp(App):
    online_c = 0
    def build(self):
	root = self.setup_gui()
        
	return root

    def setup_gui(self):
	
	self.layout =  FloatLayout(size=(300, 300))
	self.online = Button(text="None",size_hint=(.06,.06),pos=(10,100))
	self.textbox = TextInput(size_hint_y=.1,pos=(0,0))
	self.textport = TextInput(hint_text="Enter port no",size_hint=(.18,.1),pos=(160,200),focus=True,multiline=False,background_color=(0,255,255,0.7),foreground_color=(255,255,255,1),font_size=17)	
	
	self.button = Button(text='Start Server By clicking Button',size_hint=(.27,.2),background_color=(0.5,0.7,1,1),pos=(360,180))
	#self.button = Button(text='Start Server',size_hint=(.5,.1))
	self.button.bind(on_press=self.start_server)
	
	
	self.label = Label(text="Server is currently down",font_size="19dp",size_hint=(.5,.5),color=(0.9,0.1,0.1,1),pos=(190,300))
	
	self.avail = Label(text="Available Clients",size_hint=(.2,.2),color=(0.1,0.9,0.1,1),font_size="19dp",pos=(10,480),readonly=True,background_color=(255,255,0,0.6))
	self.cl_conn = TextInput(text="NONE ",size_hint=(.7,.1),foreground_color=(0.1,0.1,0.9,1),pos=(160,500))
	
	self.layout.add_widget(self.cl_conn)
	self.layout.add_widget(self.avail)
	self.layout.add_widget(self.label)
	self.layout.add_widget(self.button)
	#self.layout.add_widget(self.textbox)
	self.layout.add_widget(self.textport)
	return self.layout

    def start_server(self,touch):
	self.label.text = 'Server Started'
	self.button.text = 'Server Started'
	
	if((self.textport.text).isdigit()):
		reactor.listenTCP(int(self.textport.text), EchoFactory(self))
		
		self.label.text = 'Server Started'
	else:
		self.label.text = 'Server Not Responding :( Enter valid port'
    	return self.label

    def on_connection(self,connection):
	self.print_message("New Client")
    
    def handle_message(self, msg):
        
        opr = msg.split("$#")[0]
        msg = msg.split("$#")[1]
        print msg
        #self.label.text  = "received:  %s\n" % msg
        self.label.text  = "received: Event\n"
        splitmsg = msg.split(":")[0]
        #curos = splitmsg.split("@")[1]
        curos = platform.system()
        if (opr.isdigit()):
            if (int(opr)==2):
                self.label.text  = "received:  %s\n" % msg
                msg = msg.split(": ")[1]
        root_dirname = "Hellosnp"
        if (int(opr)==2):
            if (curos=='Linux'):
                output = subprocess.Popen(["find","/home/","-name",msg+"*"],stdout=subprocess.PIPE).communicate()[0]
                msg = opr + "$#"  + output
            if (curos=='Windows'):
                #os.chdir('C:\\Users\\Varun Malhotra\\Desktop\\')
                
                output = subprocess.Popen(["dir","/s","/a","/b",msg+"*"],shell=True,stdout=subprocess.PIPE).communicate()[0]
                msg = opr + "$#" + output
                #print msg
        if (int(opr)==4):
            msg = opr + "$#" + msg
        if (int(opr)==5):
            msg = opr + "$#" + str(self.cl_conn.text)
        if (int(opr)==8):
            msg = opr + "$#" + "lol"
            self.label.text  = "received:  %s\n" % msg
        return msg

    def client_conn(self,conn_info):
        self.cl_conn.text = ""
        #y=20
        #on=0
        
        for t in conn_info:
            #self.onlines = self.onlines + on
            #self.onlines = Button(text="yes",size_hint=(.06,.06),pos=(10,400-y))
            #self.layout.add_widget(self.onlines)
            self.cl_conn.text = self.cl_conn.text + str(t) + " , "
            #y=y+40
            #on=on+1
        #global online_c
        #online_c = on
        if (self.cl_conn.text==""):
            self.cl_conn.text = "None Available"
        
        return self.layout
		

if __name__ == '__main__':
    
    TwistedServerApp().run()

