#! /usr/bin/env python
# coding:utf-8

import cv2
import cv2.cv as cv

class KeyMap:
	# directions
	up_key 		= 65362
	down_key 	= 65364
	left_key	= 65361
	right_key	= 65363
	# special :D
	space		= 32
	enter		= 10
	backspace	= 65288
	escape		= 27
	left_ctrl	= 65507
	right_ctrl	= 65508
	left_alt	= 65513
	right_alt	= 65027
	left_shift	= 65505
	right_shift	= 65506
	tab		= 9
	caps_lock	= 65509
	insert		= 65379
	home		= 65360
	delete		= 3014656
	end		= 65367
	page_up		= 65365
	page_down	= 65366
	# letters
	q_key		= 113
	w_key		= 119
	e_key		= 101
	r_key		= 114
	t_key		= 116
	z_key		= 122
	u_key		= 117
	i_key		= 105
	o_key		= 111
	p_key		= 112
	
	a_key		= 97
	s_key		= 115
	d_key		= 100
	f_key		= 102
	g_key		= 103
	h_key		= 104
	j_key		= 106
	k_key		= 107
	l_key		= 108
	
	y_key		= 121
	x_key		= 120
	c_key		= 99
	v_key		= 118
	b_key		= 98
	n_key		= 110
	m_key		= 109
	# numbers
	number_1_key	= 43
	number_2_key	= 492
	number_3_key	= 441
	number_4_key	= 488
	number_5_key	= 504
	number_6_key	= 446
	number_7_key	= 253
	number_8_key	= 225
	number_9_key	= 237
	number_0_key	= 233
	# functional
	F1_key		= 65470
	F2_key		= 65471
	F3_key		= 65472
	F4_key		= 65473
	F5_key		= 65474
	F6_key		= 65475
	F7_key		= 65476
	F8_key		= 65477
	F9_key		= 65478
	F10_key		= 65479
	F11_key		= 65480
	F12_key		= 65481
	# other
	minus_key	= 61
	plus_key	= 65105
	# combinations
	shift_1_combination	= 65585
	shift_2_combination	= 65586
	shift_3_combination	= 65587
	shift_4_combination	= 65588
	shift_5_combination	= 65589
	shift_6_combination	= 65590
	shift_7_combination	= 65591
	shift_8_combination	= 65592
	shift_9_combination	= 65593
	shift_0_combination	= 65584


	def pressKey(self):
		return cv2.waitKey(0)

"""
km = KeyMapper()
cv.NamedWindow( "my_window", cv.CV_WINDOW_AUTOSIZE )
while True:	
	"press any key (ESC - end)"
	key_code = km.pressKey()
	if KeyMapper.escape == key_code:
		print "end"
		break
	print "key code:", key_code
#"""
