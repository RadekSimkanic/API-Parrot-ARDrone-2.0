#! /usr/bin/env python
# coding:utf-8

import socket
import threading
import struct
import time
import cv2
import cv2.cv as cv # for old code

from Config import Config
from Led import Led
from Anim import Anim


class ARDrone2:
	"""
	Controll ARDrone
	
	Třída, která slouží k získávání navigačních dat a ovládání drona.
	Video není zahrnuto, je však možné jej získat za pomoci OpenCV
	
	Inspirace byla u ARDVentur
	Inspiration by ARDVentur
	"""
	DRONE_IP = "192.168.1.1"
	
	NAVDATA_PORT = 5554
	VIDEO_PORT = 5555
	COMMAND_PORT = 5556
	CRITICAL_DATA_PORT = 5559 # not implement yet
	
	NAVDATA_PROTOCOL = "udp"
	VIDEO_PROTOCOL = "tcp"
	COMMAND_PROTOCOL = "udp"
	CRITICAL_DATA_PROTOCOL = "tcp"
	
	WATCHDOG_TIMER = 0.2
	
	def __init__( self ):
		self.sequence_number = 1
		self.speed = 0.2
		
		self.navdata = dict()
		self.image = None
		
		# spustit zachytávání streamu
		self.stream = cv2.VideoCapture( "%s://%s:%i" % ( self.VIDEO_PROTOCOL, self.DRONE_IP, self.VIDEO_PORT ) )
		self.live_video = False
		self.thread_video = threading.Thread( target = self._runVideo )
		self.thread_video.start()
		
		# spustit nasloucháni navdat
		self.navdataDemo()
		self.live_navdata = False
		self.thread_navdata = threading.Thread( target = self._runNavdata )
		self.thread_navdata.start()
		
		# spustit watchdog
		self.live_watchdog = False
		self.thread_watchdog = threading.Thread( target = self._runWatchdog )
		self.thread_watchdog.start()
		
		
	
	###### VIDEO ######
	
	def getActualFrame( self ):
		"""
		[CZE] Aktuální frame z video streamu drona.
		[ENG] 
		"""
		return self.image
	
	def getActualResolution( self ):
		"""
		[CZE] Aktuální rozlišení video streamu.
		[ENG] Inicialization the drone
		"""
		if self.image is None:
			return (0, 0)
		return (self.image.shape[0], self.image.shape[1])
	
	###### HIGH LEVEL COMMANDS ######
	
	def navdataDemo( self ):
		"""
		[CZE] Inicializace drona
		[ENG] Inicialization the drone
		"""
		self.atConfig( Config.GENERAL_NAVDATA_DEMO, "TRUE" )
	
	def setSpeed( self, speed ):
		"""
		[CZE] Nastavení rychlosti
		[ENG] Set the drone's speed
		@param	speed
			[CZE] Rychlost [0..1]
			[ENG] Speed [0..1]
		"""
		if speed >= 0 or speed <= 1:
			self.speed = speed
	
	def trim( self ):
		"""
		[CZE] Alias pro atFtrim. Vynulování hodnot gyroskopu.
		[ENG] Alias for atFtrim.
		"""
		self.atFtrim()
	
	def takeoff( self ):
		"""
		[CZE] Vzlétnutí
		[ENG]
		"""
		self.trim()
		self.atConfig( Config.CONTROL_ALTITUDE_MAX, 20000 )
		self.hover()
		self.atRef( True )
	def land( self ):
		"""
		[CZE] Přistání
		[ENG]
		"""
		self.atRef( False )
	
	def hover( self ):
		"""
		[CZE] Vznášení na místě
		[ENG]
		"""
		self.atPcmd( False, 0, 0, 0, 0 )
		
	def moveLeft( self ):
		"""
		[CZE] Nahnutí vlevo
		[ENG]
		"""
		self.atPcmd( True, -self.speed, 0, 0, 0 )
		
	def moveRight( self ):
		"""
		[CZE] Nahnutí vpravo
		[ENG]
		"""
		self.atPcmd( True, self.speed, 0, 0, 0 )
		
	def moveLeftTMP( self ):
		"""
		TEST
		"""
		self.atPcmdMag( True, 0, 0, 0, -self.speed, 0, 1 )
		
	def moveRightTMP( self ):
		"""
		TEST
		"""
		self.atPcmdMag( True, 0, 0, 0, self.speed, 0, -1 )
	
	def moveBackward( self ):
		"""
		[CZE] Nahnutí vzad
		[ENG]
		"""
		self.atPcmd( True, 0, self.speed, 0, 0 )
	
	
	def moveForward( self ):
		"""
		[CZE] Nahnutí vpřed
		[ENG]
		"""
		self.atPcmd( True, 0, -self.speed, 0, 0 )
	
		
	def moveDown( self ):
		"""
		[CZE] Klesání
		[ENG]
		"""
		self.atPcmd( True, 0, 0, -self.speed, 0 )
		
	def moveUp( self ):
		"""
		[CZE] Stoupání
		[ENG]
		"""
		self.atPcmd( True, 0, 0, self.speed, 0 )
	
	def turnLeft( self ):
		"""
		[CZE] Otočení vlevo
		[ENG]
		"""
		self.atPcmd( True, 0, 0, 0, -self.speed )
		
	def turnRight( self ):
		"""
		[CZE] Otočení vpravo
		[ENG]
		"""
		self.atPcmd( True, 0, 0, 0, self.speed )
	
	def emergency( self ):
		"""
		[CZE] emergency - vypnutí motorů
		[ENG] emergency
		"""
		self.atRef( False, True )
		self.atRef( False, False )
		
	def readyToStart( self ):
		"""
		[CZE] vypnuti emergency módu a připravit opět k vzlétnutí.
		[ENG] reset emergency mode and prepare to takeoff.
		"""
		self.atRef( False, True )
		
	def watchdog( self ):
		"""
		[CZE] Alias pro atComwdg
		[ENG] Alias for atComwdg
		"""
		self.atComwdg()
	
	def halt( self ):
		"""
		[CZE] Vypnutí drona
		[ENG] Shutdown the drone
		"""
		self._stopNavdata()
		self._stopWatchdog()
		self._stopVideo()
	
	###### LOW LEVEL AT COMMANDS ######
	def sendAt( self, command, params, seq = None ): 
		"""
		[CZE] Sestavení a poslání hotového AT příkazu do ARDrone
		[ENG] Make and sends completed AT commands into ARDrone
		
		@param	command	
			[CZE] AT příkaz
			[ENG] AT command
		@param	params
			[CZE] Parametry příkazu
			[ENG] 
		@param	seq
			[CZE] Pořadové číslo příkazu (je-li None [default] pak se bere interní číslování)
			[ENG]
		
		"""
		
		param_str = ""
		for p in params:
			if type(p) == int:
				param_str += ",%d" % p
			elif type(p) == float:
				param_str += ",%d" % f2i(p)
			elif type(p) == str:
				param_str += ",\"" + p + "\""
		
		if seq == None: 
			seq = self.sequence_number
			self.sequence_number += 1
		
		msg = "AT*%s=%i%s\r" % (command, seq, param_str)
		# odeslání socketem
		sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		sock.sendto( msg, ( self.DRONE_IP, self.COMMAND_PORT ) )
	
	def atRef( self, takeoff = False, emergency = False): # kapitola 6.5
		"""
		[CZE] Základní ovládání drona (vzlétnutí/přistání, emergency/zrušení emergency)
		[ENG] Controls the basic behaviour of the drone (take-off/landing, emergency stop/reset)
		
		@param	takeoff
			[CZE] True: vzlétnutí / False přistání
			[ENG] True: Takeoff / False: Land
		@param emergency
			[CZE] True: Nouzové vypnutí motorů nebo reset emergency / False: Vzlétnutí nebo přistání
			[ENG] True: Turn of the engines / False: Takeoff or Land
		"""
		p = 0b10001010101000000000000000000
		if takeoff:
			p += 0b1000000000
		if emergency:
			p += 0b0100000000
		
		self.sendAt( "REF", [ int( p ) ] )
	
	def atPcmd( self, progresive, left_right, front_back, vertical_speed, angular_speed ):
		"""
		[CZE] Pohyb drona
		[ENG] Send progressive commands - makes the drone move (translate/rotate).
		
		@param	progresive
			[CZE] Flag umožňující využívání progresivních příkazů a/nebo režimu kombinované s modem Yaw (bitové pole)
			[ENG] Flag enabling the use of progressive commands and/or the Combined Yaw mode (bitfield)
		@param	left_right
			[CZE] Náklonění drona vlevo-vpravo - float hodnota v rozmezí [-1..1]
			[ENG] Drone left-right tilt - floating-point value in range [−1..1]
		@param	front_back
			[CZE] Náklonění drona vpřed-vzad - float hodnota v rozmezí [-1..1]
			[ENG] Drone front-back tilt - floating-point value in range [−1..1]
		@param	vertical_speed
			[CZE] Rychlost stoupání drona - float hodnota v rozmezí [-1..1]
			[ENG] Drone vertical speed - floating-point value in range [−1..1]
		@param	angular_speed
			[CZE] Rychlost natočení drona - float hodnota v rozmezí [-1..1]
			[ENG] Drone angular speed - floating-point value in range [−1..1]
		"""
		pr = 0
		if progresive:
			pr = 1
		
		p = [ pr, float( left_right ), float( front_back ), float( vertical_speed ), float( angular_speed ) ]
		
		self.sendAt( "PCMD", p )
		
	
	def atPcmdMag( self, progresive, left_right, front_back, vertical_speed, angular_speed, magneto_psi = 0, magneto_psi_accuracy = 0 ):
		"""
		[CZE] Pohyb drona
		[ENG] Send progressive commands - makes the drone move (translate/rotate).
		
		@param	progresive
			[CZE] Flag umožňující využívání progresivních příkazů a/nebo režimu kombinované s modem Yaw (bitové pole)
			[ENG] Flag enabling the use of progressive commands and/or the Combined Yaw mode (bitfield)
		@param	left_right
			[CZE] Náklonění drona vlevo-vpravo - float hodnota v rozmezí [-1..1]
			[ENG] Drone left-right tilt - floating-point value in range [−1..1]
		@param	front_back
			[CZE] Náklonění drona vpřed-vzad - float hodnota v rozmezí [-1..1]
			[ENG] Drone front-back tilt - floating-point value in range [−1..1]
		@param	vertical_speed
			[CZE] Rychlost stoupání drona - float hodnota v rozmezí [-1..1]
			[ENG] Drone vertical speed - floating-point value in range [−1..1]
		@param	angular_speed
			[CZE] Rychlost natočení drona - float hodnota v rozmezí [-1..1]
			[ENG] Drone angular speed - floating-point value in range [−1..1]
		@param	magneto_psi NOT IMPLEMENT
			[CZE] 
			[ENG] Magneto psi (only for AT*PCMD_MAG) - floating-point value in range [−1..1]
		@param	magneto_psi_accuracy NOT IMPLEMENT
			[CZE] 
			[ENG] Magneto psi accuracy (only for AT*PCMD_MAG) - floating-point value in range [−1..1]
		"""
		pr = 0
		if progresive:
			pr = 1
		
		p = [ pr, float( left_right ), float( front_back ), float( vertical_speed ), 
			float( angular_speed ), float( magneto_psi ), float( magneto_psi_accuracy ) ]
		
		self.sendAt( "PCMD_MAG", p )
	
	def atFtrim( self ):
		"""
		[CZE] Flat trims - signal pro označení, že dron leží v rovině. Vynulování hodnot gyroskopu.
		[ENG] Flat trims - Tells the drone it is lying horizontally
		"""
		self.sendAt( "FTRIM", [] )
	
	def atCalib( self, device = 0):
		"""
		[CZE] Kalibrace mgnetometru.
		[ENG] Magnetometer calibration - Tells the drone to calibrate its magnetometer
		
		@param	device
			[CZE] ID zařízení ke kalibraci [0 - magnetometer]
			[ENG] Identifier of the device to calibrate [0 - magnetometer]
		"""
		self.sendAt( "CALIB", [ int( device ) ] )
	
	def atConfig( self, name, value):
		"""
		[CZE] Nastavení konfigurace drona
		[ENG] Sets an configurable option on the drone
		
		@param	name
			[CZE] Název konfigurace
			[ENG] the name of the option to set

		@param	value
			[CZE] Hodnota
			[ENG] the option value
		"""
		self.sendAt( "CONFIG", [ str( name ), str( value ) ] )
	
	def atConfigIds( self, session_id, user_id, application_id ):
		"""
		[CZE] Identifikátory pro následující příkaz AT*CONFIG
		[ENG] Identifiers for the next AT*CONFIG command
		
		@param	session_id
			[CZE] Id sezení
			[ENG] Current session id
		@param	user_id
			[CZE] Id uživatele
			[ENG] Current user id
		@param	application_id
			[CZE] Id aplikace
			[ENG] Current application id
		"""
		self.sendAt( "CONFIG_IDS", [ str( session_id ), str( user_id ), str( application_id ) ] )
	
	def atComwdg( self ):
		"""
		[CZE] Udržování komunikace - hlídací pes
		[ENG] Reset communication watchdog
		"""
		self.sendAt( "COMWDG", [] )
	
	def atLed( self, animation_id, frequence, duration ):
		"""
		[CZE] Spuštění LED diodové animace.
		[ENG] Sets the drone control loop PID coefficients
		
		@param	animation_id
			[CZE] Id animace
			[ENG] Animation id
		@param	frequence
			[CZE] Frekvence animace v Hz (float)
			[ENG] Frequence in Hz of the animation (float)
		@param	duration
			[CZE] Po kolika vteřinách ukončit animaci
			[ENG] Total duration in seconds of the animation
		"""
		self.sendAt( "LED", [ int( animation_id ), float( frequence ), int( duration ) ] )
		
	def atAnim( self, animation_id, duration ):
		"""
		[CZE] Spuštění pohybové animace, respektive provádění daného pohybu po určitou dobu.
		[ENG] Makes the drone execute a predefined movement (called animation).
		
		@param	animation_id
			[CZE] Id animace
			[ENG] Animation id
		@param	duration
			[CZE] Po kolika vteřinách ukončit animaci
			[ENG] Total duration in seconds of the animation
		"""
		self.sendAt( "ANIM", [ int( animation_id ), int( duration ) ] )
		
	###### STATUS/INFO METHODS ######
	
	def statusBattery(self):
		"""
		[CZE] Stav baterie (v procentech)
		[ENG] 
		"""
		return self.navdata.get(0, dict()).get('battery', 0)
		
	def statusSetSpeed(self):
		"""
		[CZE] Aktuálně nastavená rychlost drona
		[ENG] 
		"""
		return self.speed
		
	def statusTheta(self):
		"""
		[CZE] Úhel theta
		[ENG] 
		"""
		return self.navdata.get(0, dict()).get('theta', 0)
		
	def statusPhi(self):
		"""
		[CZE] Úhel phi
		[ENG] 
		"""
		return self.navdata.get(0, dict()).get('phi', 0)
	
	def statusPsi(self):
		"""
		[CZE] Úhel psi
		[ENG] 
		"""
		return self.navdata.get(0, dict()).get('psi', 0)
		
	def statusAltitude(self):
		"""
		[CZE] Nadmořská výškas
		[ENG] 
		"""
		return self.navdata.get(0, dict()).get('altitude', 0)
		
	def statusVX(self):
		"""
		[CZE] 
		[ENG] 
		"""
		return self.navdata.get(0, dict()).get('vx', 0)
		
	def statusVY(self):
		"""
		[CZE] 
		[ENG] 
		"""
		return self.navdata.get(0, dict()).get('vy', 0)
		
	def statusVZ(self):
		"""
		[CZE] 
		[ENG] 
		"""
		return self.navdata.get(0, dict()).get('vz', 0)
	
	def statusFrames(self):
		"""
		[CZE] 
		[ENG] 
		"""
		return self.navdata.get(0, dict()).get('num_frames', 0)
	
	###### NETWORK COMMUNICATIONS ######
	
	def _runNavdata( self ):
		"""
		[CZE]  
		[ENG] 
		"""
		if self.live_navdata:
			return
		
		print "RUN NAVDATA"
		
		self.navdataInit()
		self.live_navdata = True
		nav_socket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		nav_socket.setblocking( 0 )
		nav_socket.bind( ( '', self.NAVDATA_PORT ) )
		nav_socket.sendto( "\x01\x00\x00\x00", ( self.DRONE_IP, self.NAVDATA_PORT ) )
		
		while self.live_navdata:
			# příjem dat
			while True and self.live_navdata:
				try:
					packet = nav_socket.recv( 65535 )
					data = self._decodeNavdata( packet )
					
					self.navdataCycle( data )
					self.navdata = data
				except IOError:
					break
			# data se posílají co 5 ms tudíž je také tak budeme i přijímat ať zbytečně nezabíjíme CPU
			time.sleep(0.005)
		
		nav_socket.close()
	
	def _stopNavdata( self ):
		"""
		[CZE]  
		[ENG] 
		"""
		self.live_navdata = False
		self.navdataDead()
		
		self.thread_navdata.join()
	
	def _decodeNavdata( self, packet ):
		"""
		[CZE] Dekodování a zaevidování navdata
		[ENG] Decoding and evidation navdata
		
		@param	packet
			[CZE] Data k dekodování
			[ENG] Data for decoding
		"""
		offset = 0
		_ =  struct.unpack_from("IIII", packet, offset)
		
		drone_state = dict()
		
		drone_state['fly_mask']             = _[1]       & 1 # FLY MASK : (0) ardrone is landed, (1) ardrone is flying
		drone_state['video_mask']           = _[1] >>  1 & 1 # VIDEO MASK : (0) video disable, (1) video enable
		drone_state['vision_mask']          = _[1] >>  2 & 1 # VISION MASK : (0) vision disable, (1) vision enable */
		drone_state['control_mask']         = _[1] >>  3 & 1 # CONTROL ALGO (0) euler angles control, (1) angular speed control */
		drone_state['altitude_mask']        = _[1] >>  4 & 1 # ALTITUDE CONTROL ALGO : (0) altitude control inactive (1) altitude control active */
		drone_state['user_feedback_start']  = _[1] >>  5 & 1 # USER feedback : Start button state */
		drone_state['command_mask']         = _[1] >>  6 & 1 # Control command ACK : (0) None, (1) one received */
		drone_state['fw_file_mask']         = _[1] >>  7 & 1 # Firmware file is good (1) */
		drone_state['fw_ver_mask']          = _[1] >>  8 & 1 # Firmware update is newer (1) */
		drone_state['fw_upd_mask']          = _[1] >>  9 & 1 # Firmware update is ongoing (1) */
		drone_state['navdata_demo_mask']    = _[1] >> 10 & 1 # Navdata demo : (0) All navdata, (1) only navdata demo */
		drone_state['navdata_bootstrap']    = _[1] >> 11 & 1 # Navdata bootstrap : (0) options sent in all or demo mode, (1) no navdata options sent */
		drone_state['motors_mask']          = _[1] >> 12 & 1 # Motor status : (0) Ok, (1) Motors problem */
		drone_state['com_lost_mask']        = _[1] >> 13 & 1 # Communication lost : (1) com problem, (0) Com is ok */
		drone_state['vbat_low']             = _[1] >> 15 & 1 # VBat low : (1) too low, (0) Ok */
		drone_state['user_el']              = _[1] >> 16 & 1 # User Emergency Landing : (1) User EL is ON, (0) User EL is OFF*/
		drone_state['timer_elapsed']        = _[1] >> 17 & 1 # Timer elapsed : (1) elapsed, (0) not elapsed */
		drone_state['angles_out_of_range']  = _[1] >> 19 & 1 # Angles : (0) Ok, (1) out of range */
		drone_state['ultrasound_mask']      = _[1] >> 21 & 1 # Ultrasonic sensor : (0) Ok, (1) deaf */
		drone_state['cutout_mask']          = _[1] >> 22 & 1 # Cutout system detection : (0) Not detected, (1) detected */
		drone_state['pic_version_mask']     = _[1] >> 23 & 1 # PIC Version number OK : (0) a bad version number, (1) version number is OK */
		drone_state['atcodec_thread_on']    = _[1] >> 24 & 1 # ATCodec thread ON : (0) thread OFF (1) thread ON */
		drone_state['navdata_thread_on']    = _[1] >> 25 & 1 # Navdata thread ON : (0) thread OFF (1) thread ON */
		drone_state['video_thread_on']      = _[1] >> 26 & 1 # Video thread ON : (0) thread OFF (1) thread ON */
		drone_state['acq_thread_on']        = _[1] >> 27 & 1 # Acquisition thread ON : (0) thread OFF (1) thread ON */
		drone_state['ctrl_watchdog_mask']   = _[1] >> 28 & 1 # CTRL watchdog : (1) delay in control execution (> 5ms), (0) control is well scheduled */
		drone_state['adc_watchdog_mask']    = _[1] >> 29 & 1 # ADC Watchdog : (1) delay in uart2 dsr (> 5ms), (0) uart2 is good */
		drone_state['com_watchdog_mask']    = _[1] >> 30 & 1 # Communication Watchdog : (1) com problem, (0) Com is ok */
		drone_state['emergency_mask']       = _[1] >> 31 & 1 # Emergency landing : (0) no emergency, (1) emergency */
		
		data = dict()
		data['drone_state'] = drone_state
		data['header'] = _[0]
		data['seq_nr'] = _[2]
		data['vision_flag'] = _[3]
		offset += struct.calcsize("IIII")
		
		while True:
			try:
				id_nr, size =  struct.unpack_from("HH", packet, offset)
				offset += struct.calcsize("HH")
			except struct.error:
				break
				
			values = []
			
			for i in range( size-struct.calcsize("HH") ):
				values.append(struct.unpack_from("c", packet, offset)[0])
				offset += struct.calcsize("c")
			# navdata_tag_t in navdata-common.h
			if id_nr == 0:
				values = struct.unpack_from("IIfffIfffI", "".join(values))
				#print "před", values
				values = dict(zip(['ctrl_state', 'battery', 'theta', 'phi', 'psi', 'altitude', 'vx', 'vy', 'vz', 'num_frames'], values))
				#print "po", values
				# convert the millidegrees into degrees and round to int, as they
				# are not so precise anyways
				for i in 'theta', 'phi', 'psi':
					#values[i] = int(values[i] / 1000)
					values[i] /= 1000
			data[ id_nr ] = values
		
		return data
	
	def _runWatchdog( self ):
		"""
		[CZE] Udržování komunikace
		[ENG]
		""" 
		if self.live_watchdog:
			return
		
		self.live_watchdog = True
		while self.live_watchdog:
			self.atComwdg()
			time.sleep( self.WATCHDOG_TIMER )
	
	def _stopWatchdog( self ):
		"""
		[CZE] Vypnutí udržování komunikace
		[ENG] 
		"""
		self.live_watchdog = False
		#join vlákna
		self.thread_watchdog.join()
		
	def _runVideo( self ):
		"""
		[CZE] Získávání aktuálních video snímku
		[ENG]
		""" 
		if self.live_video:
			return
		
		self.videoBufferInit()
		self.live_video = True
		while self.live_video:
			ret, image = self.stream.read()
			if ret:
				self.image = image[:]
				self.videoBufferCycle( image[:] )
			else:
				print "NO IMAGE", image
				self.image = None
				self.videoBufferCycle( None )
			time.sleep(0.001)
			
			
	
	def _stopVideo( self ):
		"""
		[CZE] Vypnutí zachytávání video streamu
		[ENG] 
		"""
		self.live_video = False
		self.videoBufferDead()
		
		self.thread_video.join()
	
	
	###### ABSTRACT METHODS ######
	
	#@abstractmethod
	def navdataInit( self ):
		"""
		[CZE] Spuštěni před spuštěním příjímání navigačních dat
		[ENG] 
		"""
		pass
	
	#@abstractmethod
	def navdataCycle( self, data ):
		"""
		[CZE] Spuštění při každém zpracování navdata
		[ENG] 
		"""
		#print data
		print "Battery:", self.statusBattery()
	
	#@abstractmethod
	def navdataDead( self ):
		"""
		[CZE] Spuštěni po ukončení příjímání navigačních dat
		[ENG] 
		"""
		pass
	
	#@abstractmethod
	def videoBufferInit( self ):
		"""
		[CZE] 
		[ENG] 
		"""
		pass
	
	#@abstractmethod
	def videoBufferCycle( self, frame ):
		"""
		[CZE] Spuštění při každém video framu
		[ENG] Running at each video frame
		"""
		if frame is not None:
			cv2.imshow("KUK", frame)
			cv2.waitKey(1)
	
	#@abstractmethod
	def videoBufferDead( self ):
		"""
		[CZE] 
		[ENG] 
		"""
		pass
	
# Functions

def f2i(f):
	"""
	Interpret IEEE-754 floating-point value as signed integer.

	@param	f
		[CZE] Číslo s desetinou čárkou
		[ENG] Floating point value
	"""
	return struct.unpack('i', struct.pack('f', f))[0]	
	
	
	
	
	
	

if __name__ == "__main__":

	import termios
	import fcntl
	import os
	import sys

	fd = sys.stdin.fileno()

	oldterm = termios.tcgetattr(fd)
	newattr = termios.tcgetattr(fd)
	newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
	termios.tcsetattr(fd, termios.TCSANOW, newattr)

	oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

	drone = ARDrone2()
	drone.setSpeed(0.4)
	try:
		while 1:
			try:
				c = sys.stdin.read(1)
				c = c.lower()
				print "Got character", c
				if c == 'a':
					drone.moveLeft()
				if c == 'd':
					drone.moveRight()
				if c == 'w':
					drone.moveForward()
				if c == 's':
					drone.moveBackward()
				if c == ' ':
					drone.land()
				if c == '\n':
					drone.takeoff()
				if c == 'q':
					drone.turnLeft()
				if c == 'e':
					drone.turnRight()
				if c == 'p':
					drone.moveUp()
				if c == 'h':
					drone.hover()
				if c == 'l':
					drone.moveDown()
				if c == 'r':
					drone.emergency()
				if c == 't':
					drone.readyToStart()
				if c == 'x':
					drone.hover()
				if c == 'y':
					drone.trim()
				if c == 'n':
					drone.moveLeftTMP()
				if c == 'm':
					drone.moveRightTMP()
				if c in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0"):
					break
			except IOError:
				pass
	finally:
		termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
		drone.halt()
	
