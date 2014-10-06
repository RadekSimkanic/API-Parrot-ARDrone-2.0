#! /usr/bin/env python
# coding:utf-8

import socket
import time
import thread
import sys
import string
import base64
import cv2
import cv2.cv as cv # for old code
import numpy as np
from numpy import array

# vlastní
from core.detection_worker.pictures_convert import PicturesConvert
from core.detection_worker.rectangles_worker import RectanglesWorker
from core.socket_server_client.Handler import Handler
from core.socket_server_client.SocketServer import SocketServer


class MyHandler(Handler):
	
	# rewrite
	def runFunction(self,  params ):
		"""
		Přepsaná abstraktní metoda, která bude volat následně metody dle param
		@param	params	List/Seznam parametrů, přičemž na nultém indexu je náze funkce
		"""
		f = params[0]
		p = []
		if len( params ) > 1:
			p = params[1:]
		#print "Klient zavolal funkci: ",f
		if f in ( "detectPeoples", "detect_peoples" ) and len(p) == 3:
			# spuštění dané funkce s danými parametry
			r = self.detectionPeoples( *p )
			# poslaní zprávy klientovi s návratovými daty provedené funkce
			self.sendMessage( "returnDetectPeoples", r )
	
	# add
	def detectionPeoples(self, width, height, data):
		"""
		Funkce na vygenerování detekčních obdélníků
		@param	width	Šířka obrázku - slouží pro rekonstrukci obrázku
		@param	height	Výška obrázku - slouží pro rekonstrukci obrázku
		@param	data	Numpy string černobilého obrázků
		
		@return	List se třemi záznamy: počet detekcí, velikost rectanglu (vždy 4 nebo 0), numpy string, 
		"""
		print "DETECTION PEOPLES"
		# rekonstrukce numpy
		np_data = np.fromstring( base64.b64decode( data ), dtype='uint8')
		# rekonstrukce správného rozlíšení
		np_data = np_data.reshape( ( int( width ), int( height ) ) )
		# detekce lidí
		pc = PicturesConvert( np_data )
		rectangles = pc.getPeopleDetection(scale=1.05)
		print "DETECTION DONE!", rectangles
		if len(rectangles) == 0:
			return ["0", "0", "0"]
		rectangles = array(rectangles)
		return [ str( rectangles.shape[0]), str( rectangles.shape[1]), base64.b64encode(rectangles.tostring() ) ]
		

class MyServer(SocketServer):
	
	# rewrite
	def clientHandler(self, client):
		"""
		Spuštění handleru k danému klientovi
		@param	client	Navazání s klientem
		"""
		client_handler = MyHandler( client )
		




if __name__ == "__main__":
	ss = MyServer(12345)
	ss.run()

