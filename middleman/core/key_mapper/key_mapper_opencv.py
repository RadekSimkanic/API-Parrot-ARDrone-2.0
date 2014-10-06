#! /usr/bin/env python
# coding:utf-8

import cv2

from key_map_opencv import KeyMap as KMcv
from key_mapper import KeyMapper as KM

class KeyMapper(KM):
	
	# default values
	key_autonomous	= KMcv.m_key	# switch on/off
	key_take_off	= KMcv.enter
	key_land	= KMcv.space
	key_emergency	= KMcv.e_key
	
	key_move_left	= KMcv.a_key
	key_move_right	= KMcv.d_key
	key_move_backward	= KMcv.s_key
	key_move_forward	= KMcv.w_key
	key_turn_left	= KMcv.j_key
	key_turn_right	= KMcv.l_key
	key_move_up	= KMcv.i_key
	key_move_down	= KMcv.k_key
	
	key_speed_up	= KMcv.plus_key
	key_speed_down	= KMcv.minus_key
	key_speed_1	= KMcv.number_1_key
	key_speed_2	= KMcv.number_2_key
	key_speed_3	= KMcv.number_3_key
	key_speed_4	= KMcv.number_4_key
	key_speed_5	= KMcv.number_5_key
	key_speed_6	= KMcv.number_6_key
	key_speed_7	= KMcv.number_7_key
	key_speed_8	= KMcv.number_8_key
	key_speed_9	= KMcv.number_9_key
	key_speed_10	= KMcv.number_0_key
	
	key_hover	= KMcv.h_key
	key_trim	= KMcv.t_key
	key_shutdown	= KMcv.x_key
	key_ready	= KMcv.r_key
	
	#rewrite
	def getPressKey(self):
		"""
		Způsob získaní stisknutého tlačítka
		"""
		return cv2.waitKey(1)
	
	
	
	
	
	
	
	
	
	
	
	
