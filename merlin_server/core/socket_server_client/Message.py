#! /usr/bin/env python
# coding:utf-8

import string

class Message:
	start_flag = "<start>"
	end_flag = "<end>"
	param_flag = "<param>"
	def __init__(self, socket, buffer_limit = 10000000): ##################### smazat socket
		self.buffer_messages = ""
		self.buffer_limit = buffer_limit
		
	def parseMessage(self):
		"""
		Rozparzování bufferu a spuštění daných funkcí
		"""
		filtered_messages = []
		#print "velikost bufferu: {0}".format( len(self.buffer_messages))
		# není-li žádná zpráva kompletní - neobsahuje <start> - pak buffer pročistit od tohoto balastu
		if self.buffer_messages.find( self.start_flag ) < 0 and len(self.buffer_messages) > 0: 
			self.buffer_messages = ""
			return filtered_messages
		# není-li žádná zpráva kompletní - neobsahuje <start> nebo <end>
		if self.buffer_messages.find( self.start_flag ) < 0 or self.buffer_messages.find( self.end_flag ) < 0: 
			return filtered_messages
		
		# nezačíná-li buffer na <start> ale obsahuje jej, pak odřiznout ten počáteční balast
		start = self.buffer_messages.find( self.start_flag )
		self.buffer_messages = self.buffer_messages[ start : len(self.buffer_messages) ]
		
		# explode podle start_flag
		messages_list = string.split( self.buffer_messages, self.start_flag )
		
		# smazat buffer, který se pak znovu naplní nekompletní poslední zprávou
		self.buffer_messages = ""
		
		
		# kontrola a zaevidování jednotlivých zpráv
		i = 0
		for message in messages_list:
			i += 1
			# vyseparování prázdných zpráv
			if len(message) == 0 :
				continue
			# vyseparování zpráv bez <end>
			if message.find( self.end_flag ) < 1:
				if len(messages_list) != i:
					continue
				else:
					# je-li poslední záznam, zaevidujeme jej zpátky do bufferu a ukončíme cyklus
					self.buffer_messages = "{0}{1}".format( self.start_flag, message )
					break
			# odstraníme <end>, rozkouskujeme a zaznamenáme
			end = message.find( self.end_flag )
			message = message[ : end ]
			message = string.split( message, self.param_flag )
			filtered_messages.append( message )
		
			# zpracování zpráv do funkcí
			self.runFunction( message )
		#print filtered_messages
		return filtered_messages
	def buildMessage( self, function, params):
		"""
		Sestavení zprávy
		@param	function	Název funkce, nebo-li datový/návratový typ či specifikace zprávy
		@param	params		List/Seznam přidavných/specifikujících parametrů
		
		@return	List/Seznam rozkouskované zprávy po volikostech 4096
		"""
		fragments = []
		params.insert(0, function)
		message = "{0}{1}{2}".format( self.start_flag, self.param_flag.join(params), self.end_flag )
		#print message
		# rozkouskovat a poslat
		length = len(message)
		if length == 0:
			return fragments
		count = length / 4096
		if count * 4096 < length:
			count += 1
		for i in range(0, count):
			end = ( i+1 ) * 4096
			if i + 1 == count:
				end = length
			fragments.append( message[ i*4096 : end] )
		return fragments
	
	def addData(self, data):
		"""
		Zaevidovaní dat do bufferu 
		@return	boolean hodnata zda bylo zaevidování dat úspěšné
		"""
		# pokud není nastaven buffer tak aby mohla zpráva obsahovat aspoň jeden přenášený znak, pakk se považuje buffer za nekonečný
		if self.buffer_limit < len( self.start_flag + self.end_flag) + 1:
			self.buffer_messages += data
			return True
			
		sum_len = len( self.buffer_messages ) + len( data )
		# je-li buffer malý, odstraníme potřebnou část z nejstarších dat
		if sum_len > self.buffer_limit:
			# jsou-li data větší než velikost bufferu, zahodíme je
			if len( data ) > self.buffer_limit:
				#print "Ztráta dat. Velikost bufferu: {0} | velikost přijatých dat: {1}".format( self.buffer_limit, len( data ) )
				return False
			start = sum_len - self.buffer_limit
			self.buffer_messages = self.buffer_messages[ start: ] + data
			return True
		self.buffer_messages += data
		return True
			
	#@abstractmethod
	def runFunction(self,  params ):
		"""
		Abstraktní metoda, která bude volat následně metody dle param
		"""
		pass
