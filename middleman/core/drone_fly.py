#! /usr/bin/env python
# coding:utf-8

import threading
import time
import cv2

import termios
import fcntl
import os
import sys

from ardrone_control_lib.ARDrone2 import ARDrone2
#from key_mapper.key_mapper import KeyMapper as KM	# Terminal control
#from key_mapper.key_mapper_opencv import KeyMapper as KM	# Open CV control
from key_mapper.key_mapper_tkinter import KeyMapper as KM	# TKinter control

class DroneFly( ARDrone2 ):
	def __init__(self, key_maps = None):
		# namapování kláves
		if key_maps is not None and isinstance(key_maps, KM):
			self.KM = key_maps
		else:
			self.KM = KM()
		# namapování kláves
		#self.keyMapping(key_maps)
		
		# inicializace drona
		ARDrone2.__init__( self )
		
		# příznaky běhu
		self.autonomous = False
		self.life_manualy = False
		self.life_autonomous = False
		
		# inicializace ovládání drona
		self.thread_controls = threading.Thread( target=self.runControls )
		
	###### DRONE CONTROLS ######
	
	def startControls( self ):
		"""
		Spuštění procesu s ovládáním drona
		"""
		self.thread_controls.start()
	
	def stopControls( self ):
		"""
		Vypnuti ručního i autonomního ovládání
		"""
		self.life_manualy = False
		self.life_autonomous = False
		#self.thread_controls.join() # NE! Jinak vyhodí výjimku
	
	def runControls( self ):
		"""
		Běh ovládání - začíná se s ručním ovládáním. 
		Autonomní ovládání je podřízené manuálnímu ovládání.
		"""
		self.runManualControl()
		
		#cv2.destroyAllWindows()
		#self.halt()
	
	def stop( self ):
		"""
		Vypnuti všeho (ovládání i video streamu)
		"""
		self.stopControls()
	
	###### MANUAL CONTROL METHODS ######
	
	def runManualControl( self ):
		"""
		Zapnutí a běh ručního ovládání.
		"""
		if self.life_manualy:
			return
		self.life_manualy = True
		self.manualControlInit()
		while self.life_manualy:
			self.keyWatcher()
			self.manualControlCycle()
			time.sleep(0.01)
		self.manualControlDead()
		
	def stopManualControl( self ):
		"""
		Vypnout ruční ovládání.
		"""
		self.life_manualy = False
		
	###### KEY WATCHER ######
	
	def keyWatcher( self ):
		"""
		Snímání kláves a provedení akcí na základě stisknuté klávesy
		"""
		actual_key = self.KM.getPressKey()
		
		# akce, které jsou povolený vždy (při zapnutém i vypnutém autonomním chování)
		
		if actual_key == self.KM.key_shutdown:
			print "VYPÍNÁM"
			self.land()
			self.halt()
			self.stop()
			
		elif actual_key == self.KM.key_ready:
			self.readyToStart()
		
		# emergency - nouzové přistání
		elif actual_key == self.KM.key_emergency:
			self.emergency()
			return False
		# přístání
		elif actual_key == self.KM.key_land:
			self.land()
			return False
		# autonomous on/off
		elif actual_key == self.KM.key_autonomous:
			self.autonomous = not self.autonomous
			if self.autonomous:
				# ukončíme run pokud běžel
				self.stopManualControl()
				# spustíme autonomitu
				self.runAutonomous()
			else:
				# ukončíme runAutonomous
				self.stopAutonomous()
				self.runManualControl()
		# akce, které jsou povoleny jen když je vypnuté autonomní chování
		elif self.autonomous == False:
			# vzlétnutí
			if actual_key == self.KM.key_take_off:
				r = self.takeoff()
				self.speed = 0.1
				
			# otočení v levo
			elif actual_key == self.KM.key_turn_left:
				self.turnLeft()
		
			# otočení v pravo 
			elif actual_key == self.KM.key_turn_right:
				self.turnRight()
			# let kupředu
			elif actual_key == self.KM.key_move_forward:
				self.moveForward()
			# let vzad
			elif actual_key == self.KM.key_move_backward:
				self.moveBackward()
			# stoupání
			elif actual_key == self.KM.key_move_up:
				self.moveUp()
			# klesání
			elif actual_key == self.KM.key_move_down:
				self.moveDown()
			# let v levo
			elif actual_key == self.KM.key_move_left:
				self.moveLeft()
		
			# let v pravo 
			elif actual_key == self.KM.key_move_right:
				self.moveRight()
			# zrychlit
			elif actual_key == self.KM.key_speed_up:
				if self.speed <= 0.9:
					self.speed += 0.1
			# zpomalit
			elif actual_key == self.KM.key_speed_down:
				if self.speed >= 0.2:
					self.speed -= 0.1
			# rychlost 0.1
			elif actual_key == self.KM.key_speed_1:
				self.speed = 0.1
			# rychlost 0.2
			elif actual_key == self.KM.key_speed_2:
				self.speed = 0.2
			# rychlost 0.3
			elif actual_key == self.KM.key_speed_3:
				self.speed = 0.3
			# rychlost 0.4
			elif actual_key == self.KM.key_speed_4:
				self.speed = 0.4
			# rychlost 0.5
			elif actual_key == self.KM.key_speed_5:
				self.speed = 0.5
			# rychlost 0.6
			elif actual_key == self.KM.key_speed_6:
				self.speed = 0.6
			# rychlost 0.7
			elif actual_key == self.KM.key_speed_7:
				self.speed = 0.7
			# rychlost 0.8
			elif actual_key == self.KM.key_speed_8:
				self.speed = 0.8
			# rychlost 0.9
			elif actual_key == self.KM.key_speed_9:
				self.speed = 0.9
			# rychlost 1.0
			elif actual_key == self.KM.key_speed_10:
				self.speed = 1.0
			# vznášení
			elif actual_key == self.KM.key_hover:
				self.hover()
			# trim - vodorovná plocha
			elif actual_key == self.KM.key_trim:
				self.trim() 
		# akce, které jsou povoleny jen při zapnutém autonomním chování
		else:
			self.autonomousKeyWatcher( actual_key )
		
		return True
	
	###### INTERNAL AUTONOMOUS METHODS ######
	
	def runAutonomous( self ):
		"""
		Zapnutí autonomního chování.
		"""
		if self.life_autonomous:
			return
		self.life_autonomous = True
		self.autonomousInit()
		while self.life_autonomous:
			self.keyWatcher()
			self.autonomousCycle()
		self.autonomousDead()
		
	def stopAutonomous( self ):
		"""
		Vypnutí autonomního chování
		"""
		self.life_autonomous = False
	
	
	###### ABSTRACT METHOD - MANUAL ######
	
	#@abstractmethod
	def manualControlInit( self ):
		"""
		Jaké akce/nastavení provést při spuštění manuálního ovládání
		"""
		print "START MANUAL CONTROL"
		# změna rychlosti drona
		self.speed = 0.3
	
	#@abstractmethod
	def manualControlCycle( self ):
		"""
		Akce prováděne při manuálním ovládání. Tato metoda se volá v každém cyklu hned po případném zpracování stisknuté klávesy.
		"""
		
	
	#@abstractmethod
	def manualControlDead( self ):
		"""
		Akce provedené při vypnutí manuálního ovládání.
		"""
		print "STOP MANUAL CONTROL"
	
	
	###### ABSTRACT METHOD - AUTONOMOUS ######
	
	#@abstractmethod
	def autonomousKeyWatcher(self, actual_key):
		"""
		Abstraktní metoda
		Nastavení klaves, které jsou použitelné jen při autonomním chování.
		@return	Slouží k upozornění (pro metodu keyWatcher), že byla zachycena klavesa v této metodě (True) či nebyla zachycena (False)
		"""
		return False
	
	#@abstractmethod	
	def autonomousInit( self ):
		"""
		Abstraktní metoda - Demo
		Jaké akce/nastavení provést při spuštění autonomního chování
		"""
		print "START AUTONOMOUS"
		# změna rychlosti drona
		self.speed = 0.6
	
	#@abstractmethod	
	def autonomousCycle( self ):
		"""
		Abstraktní metoda - Demo
		Akce prováděne při autonomním chování. Tato metoda se volá v každém cyklu hned po případném zpracování stisknuté klávesy
		"""
		image = self.getActualFrame()
		if type(image) != type(False):
			cv2.imshow("detection_window", image)
		
		self.turnRight()
	
	#@abstractmethod
	def autonomousDead( self ):
		"""
		Abstraktní metoda - Demo
		Akce provedené při vypnutí autonomního chování.
		"""
		print "STOP AUTONOMOUS"
	
	

def main():
	#cv.NamedWindow( "my_window", cv.CV_WINDOW_AUTOSIZE )#cv.CV_WINDOW_AUTOSIZE
	#cv.WaitKey(0)
	
	drone_controls = DroneFly()
	drone_controls.startControls()
	
	print "Ok."

if __name__ == '__main__':
	main()
	#pass
