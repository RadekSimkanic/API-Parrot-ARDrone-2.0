#! /usr/bin/env python
# coding:utf-8

import socket
import time
import thread
import string
import base64

from Message import Message
		
class Client(Message):
	"""
	Socket Client - je potřeba nadefinovat (po zdědění) metodu clientHandler
	"""
	def __init__(self, host, port, buffer_limit = 10000000):
		"""
		Inicializace - připojení k serveru
		@param	host	Vzdálený server
		@param	port	Port vzdáleného serveru
		"""
		self.socket = socket.socket()
		self.socket.connect((host, port))
		self.buffer_complet_messages = []
		
		self.buffer_limit = buffer_limit
		self.buffer_messages = ""
	
	def waitingForReply(self, reply_function, identification_param):
		"""
		Čekání na příjem kompletní odpovědi ze serveru
		"""
		
		try:
			#i = 0
			while True:
				#i+=1
				#print i, self.buffer_complet_messages
				# kontrola zda je již přijatá správná zpráva
				for message in self.buffer_complet_messages:
					# kontrola zda má zpráva velikost aspoň 1
					if len(message) < 1:
						#smažeme a jedem dál
						self.buffer_complet_messages.remove(message)
						continue
					
					#shoduje-li se název funkce
					if message[0] == reply_function:
						if identification_param != None and len(message) < 2:
							#nemažeme, může se hodit pro někoho jiného
							continue
						if identification_param != None:
							if message[1] == identification_param:
								continue
							else:
								#smažeeme a vrátime
								self.buffer_complet_messages.remove(message)
								return message
						self.buffer_complet_messages.remove(message)
						return message
						
					
				# čekání na data od klienta
				data = self.socket.recv(4096)#65535
				#print "data",data
				# zaevidování dat do bufferu
				self.addData( data )
				# operace na základě získaných dat v bufferu
				m = self.parseMessage()
				self.buffer_complet_messages += m
				
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
		Poslaní zprávy na server
		@param	function	Název funkce, nebo-li datový/návratový typ či specifikace zprávy
		@param	params		List/Seznam přidavných/specifikujících parametrů
		"""
		fragments = self.buildMessage(function, params)
		for fragment in fragments:
			self.socket.send( fragment )
		
	
	def sendMessageWaiting( self, function, params, reply_function, identification_param = None):
		"""
		Poslaní zprávy na server a čekání na odpověď
		@param	function	Název funkce, nebo-li datový/návratový typ či specifikace zprávy
		@param	params		List/Seznam přidavných/specifikujících parametrů
		@param	reply_function	Název funkce návratové zprávy
		@param	identification_param	Číselná hodnota identifikace zprávy (musí byt jako první parametr - hned po názvu funkce)
		
		@return	návrat rozparzované zprávy
		"""
		self.sendMessage( function, params )
		return self.waitingForReply( reply_function, identification_param )
		
