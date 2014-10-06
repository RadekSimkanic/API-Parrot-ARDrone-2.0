#! /usr/bin/env python
# coding:utf-8

import termios
import fcntl
import os
import sys

from key_map_terminal import KeyMap as KMt

class KeyMapper:
	# names for remapping via keyMapping
	KEY_MAP_AUTONOMOUS	= "key_autonomous"
	KEY_MAP_TAKE_OFF	= "key_take_off"
	KEY_MAP_LAND		= "key_land"
	KEY_MAP_EMERGENCY	= "key_emergency"
	KEY_MAP_MOVE_LEFT	= "key_move_left"
	KEY_MAP_MOVE_RIGHT	= "key_move_right"
	KEY_MAP_MOVE_BACKWARD	= "key_move_backward"
	KEY_MAP_MOVE_FORWARD	= "key_move_forward"
	KEY_MAP_MOVE_UP		= "key_move_up"
	KEY_MAP_MOVE_DOWN	= "key_move_down"
	KEY_MAP_TURN_LEFT	= "key_turn_left"
	KEY_MAP_TURN_RIGHT	= "key_turn_right"
	KEY_MAP_SPEED_UP	= "key_speed_up"
	KEY_MAP_SPEED_DOWN	= "key_speed_down"
	KEY_MAP_SPEED_1		= "key_speed_1"
	KEY_MAP_SPEED_2		= "key_speed_2"
	KEY_MAP_SPEED_3		= "key_speed_3"
	KEY_MAP_SPEED_4		= "key_speed_4"
	KEY_MAP_SPEED_5		= "key_speed_5"
	KEY_MAP_SPEED_6		= "key_speed_6"
	KEY_MAP_SPEED_7		= "key_speed_7"
	KEY_MAP_SPEED_8		= "key_speed_8"
	KEY_MAP_SPEED_9		= "key_speed_9"
	KEY_MAP_SPEED_10	= "key_speed_10"
	KEY_MAP_HOVER		= "key_hover"
	KEY_MAP_TRIM		= "key_trim"
	KEY_MAP_SHUTDOWN	= "key_shutdown"
	KEY_MAP_READY		= "key_ready"
	
	# default values
	key_autonomous	= KMt.m_key	# switch on/off
	key_take_off	= KMt.enter
	key_land	= KMt.space
	key_emergency	= KMt.e_key
	
	key_move_left	= KMt.a_key
	key_move_right	= KMt.d_key
	key_move_backward	= KMt.s_key
	key_move_forward	= KMt.w_key
	key_turn_left	= KMt.j_key
	key_turn_right	= KMt.l_key
	key_move_up	= KMt.i_key
	key_move_down	= KMt.k_key
	
	key_speed_up	= KMt.plus_key
	key_speed_down	= KMt.minus_key
	key_speed_1	= KMt.number_1_key
	key_speed_2	= KMt.number_2_key
	key_speed_3	= KMt.number_3_key
	key_speed_4	= KMt.number_4_key
	key_speed_5	= KMt.number_5_key
	key_speed_6	= KMt.number_6_key
	key_speed_7	= KMt.number_7_key
	key_speed_8	= KMt.number_8_key
	key_speed_9	= KMt.number_9_key
	key_speed_10	= KMt.number_0_key
	
	key_hover	= KMt.h_key
	key_trim	= KMt.t_key
	key_shutdown	= KMt.x_key
	key_ready	= KMt.r_key
	
	def __init__(self, key_maps = None):
		self.keyMapping(key_maps)
		
	def keyMapping( self, key_map = None ):
		"""
		Namapování/nastavení ovladacích kláves. Změní se jen ty které jsou ve slovníku. Neřeší se kolize!
		@param	key_map	slovnik mapující klávesy
		"""
		if key_map == None or type(key_map) != type({}):
			return
		# přemapování
		for name, code in key_map.items():
			if name == self.KEY_MAP_AUTONOMOUS:
				self.key_autonomous	= code
			elif name == self.KEY_MAP_TAKE_OFF:
				self.key_take_off	= code
			elif name == self.KEY_MAP_LAND:
				self.key_land		= code
			elif name == self.KEY_MAP_EMERGENCY:
				self.key_emergency	= code
		
			elif name == self.KEY_MAP_MOVE_LEFT:
				self.key_move_left	= code
			elif name == self.KEY_MAP_MOVE_RIGHT:
				self.key_move_right	= code
			elif name == self.KEY_MAP_MOVE_BACKWARD:
				self.key_move_backward	= code
			elif name == self.KEY_MAP_MOVE_FORWARD:
				self.key_move_forward	= code
			elif name == self.KEY_MAP_TURN_LEFT:
				self.key_turn_left	= code
			elif name == self.KEY_MAP_TURN_RIGHT:
				self.key_turn_right	= code
			elif name == self.KEY_MAP_MOVE_UP:
				self.key_move_up	= code
			elif name == self.KEY_MAP_MOVE_DOWN:
				self.key_move_down	= code
		
			elif name == self.KEY_MAP_SPEED_UP:
				self.key_speed_up	= code
			elif name == self.KEY_MAP_SPEED_DOWN:
				self.key_speed_down	= code
			elif name == self.KEY_MAP_SPEED_1:
				self.key_speed_1	= code
			elif name == self.KEY_MAP_SPEED_2:
				self.key_speed_2	= code
			elif name == self.KEY_MAP_SPEED_3:
				self.key_speed_3	= code
			elif name == self.KEY_MAP_SPEED_4:
				self.key_speed_4	= code
			elif name == self.KEY_MAP_SPEED_5:
				self.key_speed_5	= code
			elif name == self.KEY_MAP_SPEED_6:
				self.key_speed_6	= code
			elif name == self.KEY_MAP_SPEED_7:
				self.key_speed_7	= code
			elif name == self.KEY_MAP_SPEED_8:
				self.key_speed_8	= code
			elif name == self.KEY_MAP_SPEED_9:
				self.key_speed_9	= code
			elif name == self.KEY_MAP_SPEED_10:
				self.key_speed_10	= code
		
			elif name == self.KEY_MAP_HOVER:
				self.key_hover		= code
		
			elif name == self.KEY_MAP_TRIM:
				self.key_trim		= code
			elif name == self.KEY_MAP_SHUTDOWN:
				self.key_shutdown	= code
			elif name == self.KEY_MAP_READY:
				self.key_ready		= code
	#@abstractmethod
	def getPressKey(self):
		"""
		Způsob získaní stisknutého tlačítka
		"""
		fd = sys.stdin.fileno()
		old = termios.tcgetattr(fd)
		new = termios.tcgetattr(fd)
		new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
		new[6][termios.VMIN] = 1
		new[6][termios.VTIME] = 0
		termios.tcsetattr(fd, termios.TCSANOW, new)
		c = None
		try:
			c = os.read(fd, 1)
		finally:
			termios.tcsetattr(fd, termios.TCSAFLUSH, old)
		return c
	
	
	
	
	
	
	
	
	
	
	
	
