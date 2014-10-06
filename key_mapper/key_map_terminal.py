#! /usr/bin/env python
# coding:utf-8

import termios
import fcntl
import os
import sys

class KeyMap:
	# directions
	"""
	up_key 		= 
	down_key 	= 
	left_key	= 
	right_key	= 
	"""
	# special :D
	space		= " "
	enter		= '\n'
	#backspace	= 65288
	#escape		= 27
	#left_ctrl	= 65507
	#right_ctrl	= 65508
	#left_alt	= 65513
	#right_alt	= 65027
	#left_shift	= 65505
	#right_shift	= 65506
	tab		= "\t"
	#caps_lock	= 65509
	#insert		= 65379
	#home		= 65360
	#delete		= 3014656
	#end		= 65367
	#page_up		= 65365
	#page_down	= 65366
	# letters
	q_key		= "q"
	w_key		= "w"
	e_key		= "e"
	r_key		= "r"
	t_key		= "t"
	z_key		= "z"
	u_key		= "u"
	i_key		= "i"
	o_key		= "o"
	p_key		= "p"
	
	a_key		= "a"
	s_key		= "s"
	d_key		= "d"
	f_key		= "f"
	g_key		= "g"
	h_key		= "h"
	j_key		= "j"
	k_key		= "k"
	l_key		= "l"
	
	y_key		= "y"
	x_key		= "x"
	c_key		= "c"
	v_key		= "v"
	b_key		= "b"
	n_key		= "n"
	m_key		= "m"
	# numbers (abstract - values)
	number_1_key	= "1"
	number_2_key	= "2"
	number_3_key	= "3"
	number_4_key	= "4"
	number_5_key	= "5"
	number_6_key	= "6"
	number_7_key	= "7"
	number_8_key	= "8"
	number_9_key	= "9"
	number_0_key	= "0"
	# number ENG keyboard
	number_1_eng_key	= "1"
	number_2_eng_key	= "2"
	number_3_eng_key	= "3"
	number_4_eng_key	= "4"
	number_5_eng_key	= "5"
	number_6_eng_key	= "6"
	number_7_eng_key	= "7"
	number_8_eng_key	= "8"
	number_9_eng_key	= "9"
	number_0_eng_key	= "0"
	# number CZE keyboard
	number_1_cze_key	= "+"
	number_2_cze_key	= "ě"
	number_3_cze_key	= "š"
	number_4_cze_key	= "č"
	number_5_cze_key	= "ř"
	number_6_cze_key	= "ž"
	number_7_cze_key	= "ý"
	number_8_cze_key	= "á"
	number_9_cze_key	= "í"
	number_0_cze_key	= "é"
	

	
	# functional
	"""
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
	"""
	# other and special abstract char
	minus_key	= "-"
	plus_key	= "+"
	exclamation_key	= "!"
	at_key		= "@"
	sharp_key	= "#"
	dollar_key	= "$"
	percent_key	= "%"
	caret_key	= "^"
	and_key		= "&"
	star_key	= "*"
	left_bracket_key	= "("
	right_bracket_key	= ")"
	double_point_key	= ":"
	point_key	= "."
	comma_key	= ","
	
	
	# combinations
	# combinations ENG keyboards
	shift_1_eng_combination	= "!"
	shift_2_eng_combination	= "@"
	shift_3_eng_combination	= "#"
	shift_4_eng_combination	= "$"
	shift_5_eng_combination	= "%"
	shift_6_eng_combination	= "^"
	shift_7_eng_combination	= "&"
	shift_8_eng_combination	= "*"
	shift_9_eng_combination	= "("
	shift_0_eng_combination	= ")"
	
	# combinations CZE keyboards
	shift_1_cze_combination	= "1"
	shift_2_cze_combination	= "2"
	shift_3_cze_combination	= "3"
	shift_4_cze_combination	= "4"
	shift_5_cze_combination	= "5"
	shift_6_cze_combination	= "6"
	shift_7_cze_combination	= "7"
	shift_8_cze_combination	= "8"
	shift_9_cze_combination	= "9"
	shift_0_cze_combination	= "0"
	
	def pressKey(self):
		"""
		fd = sys.stdin.fileno()

		oldterm = termios.tcgetattr(fd)
		newattr = termios.tcgetattr(fd)
		newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
		termios.tcsetattr(fd, termios.TCSANOW, newattr)

		oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
		c = sys.stdin.read(1)
		return c.lower()
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
			print "VYJIMKA===================="
			termios.tcsetattr(fd, termios.TCSAFLUSH, old)
		return c

"""
km = KeyMapper()
while True:	
	"press any key (ESC - end)"
	key_code = km.pressKey()
	if KeyMapper.escape == key_code:
		print "end"
		break
	print "key code:", key_code
#"""
