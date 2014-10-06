#! /usr/bin/env python
# coding:utf-8


import cv2
import cv2.cv as cv
import numpy
from multiprocessing import Process, Lock
import subprocess
import time

import socket

from my_client import MyClient
from core.drone_fly import DroneFly
from core.detection_worker.pictures_convert import PicturesConvert
from core.detection_worker.rectangles_worker import RectanglesWorker
from core.detection_worker.frames_worker import FramesWorker
from core.hybrid_ring_buffer import HybridRingBuffer
#from core.socket_server import *

def clock():
	return cv2.getTickCount() / cv2.getTickFrequency()

class DronePeopleDetection( DroneFly ):
	# velikost detekčního obdélníku pro oddálení
	MAXIMUM_WIDTH_DETECTION = 180
	# velikost detekčního obdélníku pro přiblížení
	MINIMUM_WIDTH_DETECTION = 140
	# velikost bufferu
	BUFFER_SIZE_1 = 8
	BUFFER_SIZE_2 = 100
	# potřeba nalezených vhodných detekcí v bufferech
	DETECTIONS_IN_BUFFER_1 = 5
	DETECTIONS_IN_BUFFER_2  = 5
	# počet 
	NUMBER_STEPS_PREDICT = 3
	# koeficient 
	MAXIMUM_STEPS_COEFFICIENT = 4
	# procentuální středová šířka ve kterém se má umísťovat střed detekce - pro natáčení drona
	ACTIVE_DETECTIONS_AREA = 10 #%
	
	SIZE_DIVERGENCE = 0.4
	POSITION_DIVERGENCE = 0.4
	
	# connection information
	PORT = 12345
	#SERVER = socket.gethostname()
	SERVER = "158.196.141.49" # merlin2
	
	
	# název okna
	WINDOW_NAME_DETECTION = "people detection"
	
		
	#rewrite
	def autonomousKeyWatcher(self, actual_key):
		"""
		Nastavení klaves, které jsou použitelné jen při autonomním chování.
		@return	Slouží k upozornění (pro metodu keyWatcher), že byla zachycena klavesa v této metodě (True) či nebyla zachycena (False)
		"""
		return False
	#rewrite
	def autonomousInit( self ):
		"""
		Abstraktní metoda - Demo
		Jaké akce/nastavení provést při spuštění autonomního chování
		"""
		print "START AUTONOMOUS"
		
		# inicializace klienta pro komunikaci se serverem
		print "MMMMMMMMMMMMMMMMMMMMMMMMMMM"
		self.client = MyClient(self.SERVER, self.PORT)
		print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXxx"
		# inicializace práce s obrázky
		self.pc = PicturesConvert()
		print "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYyyyyyyyyyy"
		# inicializace práce s detekčními obdélníky
		self.rw = RectanglesWorker()
		print "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"
		# inicializace práce s framy obsahující detekční obdélníky
		self.fw = FramesWorker()
		print "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
		# inicializace bufferů
		self.hrb_1 = HybridRingBuffer( self.BUFFER_SIZE_1 )
		self.hrb_2 = HybridRingBuffer( self.BUFFER_SIZE_2 )
		print "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK"
		# vznášet se na místě
		self.hover()
		print "LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL"
		# změna rychlosti drona
		self.setSpeed( 0.1 )
	#rewrite
	def autonomousDead( self ):
		"""
		Abstraktní metoda - Demo
		Akce provedené při vypnutí autonomního chování.
		"""
		print "STOP AUTNOMOUS"
		
	#rewrite
	def autonomousCycle( self ):
		"""
		Abstraktní metoda - Demo
		Akce prováděne při autonomním chování. Tato metoda se volá v každém cyklu hned po případném zpracování stisknuté klávesy
		"""
		print "AUTONOMOUS CYCLE"
		image = self.getActualFrame()
		if type(image) != type(False):
			start_detection = clock()
			self.pc.setPicture( image )
			gray = self.pc.getGray()
			# získání detekce ze serveru
			r = self.client.detectionPeoples( gray )
			stop_detection = clock()
			
			# korekce velikosti
			self.rw.setRectangles( r )
			r = self.rw.correctionRectangles()
			
			# zaznamenání framu do kruhového bufferu
			self.hrb_1.add( r )
			# nastavit práci s framy zaevidované v kruhovém bufferu
			self.fw.setFrames( self.hrb_1.getAllItems() )
			# zprůměrovat podobné obdélníky jednotlivě ve všech frámech
			self.fw.averagingAppropriateRectangles(buble_mode = False)
			# odfiltrování ustřelených detekčních obdélníků
			r1 = self.fw.filteringIncorrectRectangles(self.BUFFER_SIZE_1, self.DETECTIONS_IN_BUFFER_1, mode_position = True)
			
			# filter pro zobrazení jen jedné detekce (detekce zájmů)
			# zaevidování vyfiltrovaného frámu
			self.hrb_2.add( r1 )
			self.fw.setFrames( self.hrb_2.getAllItems() )
			params = {
				"find_in_buffer"	: self.DETECTIONS_IN_BUFFER_2, 
				"number_steps_predict"	: self.NUMBER_STEPS_PREDICT, 
				"maximum_step"	: self.MAXIMUM_STEPS_COEFFICIENT,
				"size_divergence"	: self.SIZE_DIVERGENCE,
				"position_divergence"	: self.POSITION_DIVERGENCE
			}
			r3 = self.fw.keyRectangle( **params )
			
			stop_processing = clock()
			
			# akce kterou má dron provést
			self.droneAction( r3 )
			
			# realtime zobrazení obrázku a detekcí - zelená: detekce zájmu; červena: všechny detekce
			self.pc.reset()
			scale = [[0, 0, self.MAXIMUM_WIDTH_DETECTION, 10],[0, 0, self.MINIMUM_WIDTH_DETECTION, 10]] # měřítko
			self.pc.drawRectangles( scale, (0, 0, 0), 2 )
			self.pc.drawRectangles( r3, (0, 255, 0), 5 )
			self.pc.drawRectangles( r, (0, 0, 255), 1 )
			cv2.imshow(self.WINDOW_NAME_DETECTION, image)
			
			print "detekce: {0} s | zpracování: {1} s".format( stop_detection - start_detection, stop_processing - stop_detection )
		
	# add
	def droneAction( self, rectangle ):
		"""
		Provedení akce podle umístění detekčního obdélníku zájmu.
		@param	rectangle	Frame s jedním (nebo žádným) detekčním obdélníkem zájmu
		"""
		if type( rectangle ) in ( type( False ), type( None ) ) or len( rectangle ) != 1 or len( rectangle[0] ) != 4:
			#print "NO ACTION!!!"
			self.hover()
			return
		# získáme hodnoty
		r = rectangle[0]
		
		width = r[2] - r[0]
		height = r[3] - r[1]
		sx = r[0] + int( width / 2 )
		sy = r[1] + int( height / 2 )
		
		# detekční hranice v okně - pro směrové natočení drona
		window_height, window_width = self.getActualResolution()
		print "resolution W/H", window_width, window_height
		left_detection_limit = int( float(window_width) / 2 - ( float(window_width) / 2 *  float(self.ACTIVE_DETECTIONS_AREA) / 100 ) )
		right_detection_limit = window_width - left_detection_limit
		# nenastane-li žádná operace pak spustit vznášení se
		set_hover = True
		#print "width SX LD RD", width, sx, left_detection_limit, right_detection_limit
		if sx < left_detection_limit:
			# je-li detekce přílíš vlevo - natočit vlevo
			print "<<<<<<<<<<<---------------", sx, left_detection_limit
			set_hover = False
			self.setSpeed(0.02) #0.01
			self.turnLeft()
			
		elif sx > right_detection_limit:
			# je-li detekce přílíš vpravo - natočit vpravo
			print "----------------------->>>>>>>>>>>>>", sx, right_detection_limit
			set_hover = False
			self.setSpeed(0.02) #0.01
			self.turnRight()
		
		if width < self.MINIMUM_WIDTH_DETECTION:
			# je-li detekce daleko - přiblížíme se
			print "##############vpřed##################", width
			set_hover = False
			self.moveForward()
		elif width > self.MAXIMUM_WIDTH_DETECTION:
			# je-li detekce přílíš blízko - oddálíme se
			print "^^^^^^^^^^^^^^vzad^^^^^^^^^^^^^", width
			set_hover = False
			self.moveBackward()
		
		# a jdeme se opět vznášet
		if set_hover:
			self.setSpeed(0.1) #0.1
			self.hover()
		
	
def main():
	drone_controls = DronePeopleDetection()
	drone_controls.startControls()

if __name__ == '__main__':
	main()

