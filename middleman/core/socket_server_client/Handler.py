#! /usr/bin/env python
# coding:utf-8

import socket
import time
import string
import base64

from Message import Message

class Handler(Message):
	"""
	Udržení spojení s daným připojeným klientem a případna jeho obsluha.
	"""
	def __init__(self, socket, buffer_limit = 10000000):
		"""
		Inicializace instance třídy
		@param	socket	Navázaný socket s klientem
		@param	buffer_limit	Velikost bufferu pro uchovávání dat
		"""
		self.buffer_messages = ""
		self.socket = socket
		self.buffer_limit = buffer_limit
		#Message.__init__( socket, buffer_limit )
		
		self.run()
	
	def __del__(self):
		self.socket.close()
		
	def run(self):
		"""
		Čekání na příjem dat od klienta, ktere se zaeviduji do bufferu, 
		rozprazuji se a na základě toho se spustí funkce a případně následně se pošle odpověď klientovi
		"""
		try:
			while True:
				# čekání na data od klienta
				data = self.socket.recv(4096)
				
				# zaevidování dat do bufferu
				self.addData( data )
				# operace na základě získaných dat v bufferu
				self.parseMessage()
				
				# pauznutí vlákna
				time.sleep(0.00000002)
		except socket.error, e:
			# A socket error
			print "Socket error"
			print e
		except IOError, e:
			if e.errno == errno.EPIPE:
				# EPIPE error
				print "Klient ukončil spojení"
				self.socket.close()
				
		    	else:
				# Other error
				print "ERROR"
				print e
				
	def sendMessage( self, function, params):
		"""
		Poslaní zprávy klientovi
		@param	function	Název funkce, nebo-li datový/návratový typ či specifikace zprávy
		@param	params		List/Seznam přidavných/specifikujících parametrů
		"""
		print "SEND", function, params
		fragments = self.buildMessage(function, params)
		for fragment in fragments:
			self.socket.send( fragment )
			
	

