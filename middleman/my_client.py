#! /usr/bin/env python
# coding:utf-8

import socket
import sys
import time
import cv2
import string
import base64
import numpy as np
from numpy import array

# for old code
import cv2.cv as cv
import zlib

# vlastní
from core.detection_worker.pictures_convert import PicturesConvert
from core.detection_worker.rectangles_worker import RectanglesWorker
from core.socket_server_client.Client import Client

def clock():
	return cv2.getTickCount() / cv2.getTickFrequency()
	

	
class MyClient(Client):
	def __init__(self, host, port):
		Client.__init__(self, host, port)
		
	
	# add
	def returnDetectionPeoples(self, width, height, data):
		"""
		Funkce na zpracování získaných detekčních obdélníků
		@param	width	Šířka matice
		@param	height	Výška matice
		@param	data	Numpy string detekčních obdélníků
		
		@return	List se třemi záznamy: počet detekcí, velikost rectanglu (vždy 4 nebo 0), numpy string, 
		"""
		#print "RETURN", data
		# kontrola zda je aspoň jedná detekce
		if int(width) == 0:
			return []
		# rekonstrukce numpy
		np_data = np.fromstring( base64.b64decode( data ), dtype='int')
		# rekonstrukce správného rozlíšení
		np_data = np_data.reshape( ( int( width ), int( height ) ) )
		print np_data
		return np_data
		
	# add
	def detectionPeoples(self, image, compress = False):
		function = "detectPeoples"
		string = image.tostring()
		if compress:
			function = "detectPeoplesCompress"
			string = string.encode( "zlib" )
		#compress = image.tostring().encode("zlib")
		base = base64.b64encode( string )
		#print "Délka dat:", len(base64.b64encode(image.tostring()) ), len(base)
		param = [ str(image.shape[0]), str(image.shape[1]), base ]
		r = self.sendMessageWaiting( function, param, "returnDetectPeoples" )
		return self.returnDetectionPeoples( *r[1:] )
	

if __name__ == "__main__":
	# inicializace obrázku
	picture = "img/Jerusalem11-094571.jpg"
	img = cv2.imread( picture )
	pc = PicturesConvert( img )
	rw = RectanglesWorker()
	img = pc.getGray()
	
	# detekce na vzdaleném serveru
	start_detection = clock()
	
	host = socket.gethostname()# Get local machine name
	port = 12345# Reserve a port for your service.
	
	mc = MyClient( host, port )
	rectangles = mc.detectionPeoples( img )
	
	stop_detection = clock()
	print( "Zpracování probíhalo: {0} s".format(stop_detection-start_detection) )
	#print "rectangles", rectangles
	pc.reset()
	pc.drawRectangles(rectangles)
	cv2.imshow( "picture", pc.getActualPicture() )
	cv.WaitKey(0)
	
	
	
	
