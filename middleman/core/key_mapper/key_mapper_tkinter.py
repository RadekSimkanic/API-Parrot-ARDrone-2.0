#! /usr/bin/env python
# coding:utf-8

import Tkinter as tk
import threading

from key_map_tkinter import KeyMap as KMtk
from key_mapper import KeyMapper as KM

class KeyMapper(KM):
	
	# default values
	key_autonomous	= KMtk.m_key	# switch on/off
	key_take_off	= KMtk.enter
	key_land	= KMtk.space
	key_emergency	= KMtk.e_key
	
	key_move_left	= KMtk.a_key
	key_move_right	= KMtk.d_key
	key_move_backward	= KMtk.s_key
	key_move_forward	= KMtk.w_key
	key_turn_left	= KMtk.j_key
	key_turn_right	= KMtk.l_key
	key_move_up	= KMtk.i_key
	key_move_down	= KMtk.k_key
	
	key_speed_up	= KMtk.plus_key
	key_speed_down	= KMtk.minus_key
	key_speed_1	= KMtk.number_1_key
	key_speed_2	= KMtk.number_2_key
	key_speed_3	= KMtk.number_3_key
	key_speed_4	= KMtk.number_4_key
	key_speed_5	= KMtk.number_5_key
	key_speed_6	= KMtk.number_6_key
	key_speed_7	= KMtk.number_7_key
	key_speed_8	= KMtk.number_8_key
	key_speed_9	= KMtk.number_9_key
	key_speed_10	= KMtk.number_0_key
	
	key_hover	= KMtk.h_key
	key_trim	= KMtk.t_key
	key_shutdown	= KMtk.x_key
	key_ready	= KMtk.r_key
	
	def __init__( self, key_map = None ):
		KM.__init__( self, key_map )
		
		self.lastPressKey = None
		self.thread_controls = threading.Thread( target=self.startTk )
		self.thread_controls.start()
		
		
	#rewrite
	def getPressKey(self):
		"""
		Způsob získaní stisknutého tlačítka
		"""
		r = self.lastPressKey
		self.lastPressKey = None
		return r
	
	#add
	def startTk(self):
		self.root = tk.Tk()
		self.root.bind_all('<Key>', self.bindKey)
		#self.root.withdraw()
		self.root.mainloop()
	
	#add
	def bindKey(self, event):
		c = event.keysym
		print c
		if c == self.key_shutdown:
			self.root.destroy()
		self.lastPressKey = c
	
	
	
	
	
	
	
	
	
	
