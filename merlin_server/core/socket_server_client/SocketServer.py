#! /usr/bin/env python
# coding:utf-8

import socket
import time
import thread
import string

	
class SocketServer:
	"""
	Socket server - je potřeba nadefinovat (po zdědění) metodu clientHandler
	"""
	def __init__(self, port):
		"""
		@param	port	Port na kterém se má naslouchat
		"""
		self.s = socket.socket()
		self.host = socket.gethostname()# Get local machine name
		self.port = port# Reserve a port for your service.
		self.stop_time = -1
	
	def setStopTime(self, time):
		"""
		Nastavení kdy se má socket server vypnout
		"""
		None #TODO
	
	def run(self):
		"""
		Spuštění čekání na připojení klientů
		"""
		# naslouchání na portu
		self.s.bind((self.host, self.port))# Bind to the port
		# čekáme na připojení klienta
		self.s.listen(5)
		while True:
			# spojení s klientem
			c, addr = self.s.accept()
			
			if self.checkTime():
				#vypnutí serveru a služeb na něm	TODO vyřešit lépe - v dalším vlákně který ho po time exceeded killne
				print "Vypínám server [time exceeded]..."
				break
			
			#spuštění obsluhy pro daného klienta
			thread.start_new_thread(self.clientHandler, (c,))
			
			print "navázáno spojení s IP: {0}".format(addr)
			c.send("Welcome to {0}".format(self.host) )
			
		print "Server byl vypnut"
	
	#@abstractmethod
	def clientHandler(self, client):
		"""
		Spuštění handleru k danému klientovi
		@param	client	Navazání s klientem
		"""
		#client_handler = Handler( client )
		pass
		
		
	def checkTime(self):
		"""
		Zjistí zda již nebyl překročen čas
		@return	True - již byl překročen čas; False - čas nepřekročen
		"""
		if self.stop_time == -1:
			return False
		
		return True
	
