#!/usr/bin/env python

import socket
import time

def tcp_client(TCP_IP='127.0.0.1',TCP_PORT=5006,MESSAGE="Hello, World!"):
	#TCP_IP = TCP_IP
	#TCP_PORT = TCP_PORT
	BUFFER_SIZE = 1024
	#MESSAGE = MESSAGE
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	s.send(MESSAGE)
	data = s.recv(BUFFER_SIZE)
	time1=time.ctime()
	s.close()
	
	print time1,"---> response from ", TCP_IP," :", data
import getpass
user=getpass.getuser()
def tcp_server(Host="localhost",PORT=5006):
	
	import SocketServer
	
	
	class MyTCPHandler(SocketServer.BaseRequestHandler):

	    """
	    The RequestHandler class for our server.
	
	    It is instantiated once per connection to the server, and must
	    override the handle() method to implement communication to the
	    client.
	    """
	    
	    def handle(self):
		global user
		# self.request is the TCP socket connected to the client
	        self.data = self.request.recv(1024).strip()
		time2=time.ctime()
	        print time2,"---> {} received the detector:".format(self.client_address[0])
		log=open("/home/{0}/IDSDector.log".format(user),"a")
		log.write("{0} ---> {1} received the detector: {2}\n".format(time2,self.client_address[0],self.data))
		print self.data
	        # just send back the same data, but upper-cased
	        self.request.sendall("Successful")#(self.data.upper())
		
	
	# Create the server, binding to localhost on port 9999
	server = SocketServer.TCPServer((Host, PORT), MyTCPHandler)
	# Activate the server; this will keep running until you interrupt the program with Ctrl-C
	server.serve_forever()
