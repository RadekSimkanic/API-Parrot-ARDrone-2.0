#! /usr/bin/env python
# coding:utf-8

import Tkinter as tk

class KeyMap:
	# directions
	up_key 		= "Up"
	down_key 	= "Down"
	left_key	= "Left"
	right_key	= "Right"
	# special :D
	space		= "space"
	enter		= "Return"
	backspace	= "BackSpace"
	escape		= "Escape"
	left_ctrl	= "Control_L"
	right_ctrl	= "Control_R"
	left_alt	= "Alt_L"
	right_alt	= "ISO_Level3_Shift"
	left_shift	= "Shift_L"
	right_shift	= "Shift_R"
	#tab		= None
	caps_lock	= "Caps_Lock"
	insert		= "Insert"
	home		= "Home"
	delete		= "Delete"
	end		= "End"
	page_up		= "Prior"
	page_down	= "Next"
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
	# numbers ENG keyboard
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
	# numbers CZE keyboard
	number_1_cze_key	= "plus"
	number_2_cze_key	= "ecaron"
	number_3_cze_key	= "scaron"
	number_4_cze_key	= "ccaron"
	number_5_cze_key	= "rcaron"
	number_6_cze_key	= "zcaron"
	number_7_cze_key	= "yacute"
	number_8_cze_key	= "aacute"
	number_9_cze_key	= "iacute"
	number_0_cze_key	= "eacute"
	# functional
	F1_key		= "F1"
	F2_key		= "F2"
	F3_key		= "F3"
	F4_key		= "F4"
	F5_key		= "F5"
	F6_key		= "F6"
	F7_key		= "F7"
	F8_key		= "F8"
	F9_key		= "F9"
	F10_key		= "F10"
	F11_key		= "F11"
	F12_key		= "F12"
	# other
	minus_key	= "minus"
	plus_key	= "plus"
	
	# combinations
	# combinations ENG keyboards
	shift_1_eng_combination	= "exclam"
	shift_2_eng_combination	= "at"
	shift_3_eng_combination	= "numbersign"
	shift_4_eng_combination	= "dollar"
	shift_5_eng_combination	= "percent"
	shift_6_eng_combination	= "asciicircum"
	shift_7_eng_combination	= "ampersand"
	shift_8_eng_combination	= "asterisk"
	shift_9_eng_combination	= "braceleft"
	shift_0_eng_combination	= "braceright"
	
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
	
	# other and special abstract char
	minus_key	= "minus"
	plus_key	= "plus"
	exclamation_key	= "exclam"
	at_key		= "at"
	sharp_key	= "numbersign"
	dollar_key	= "dollar"
	percent_key	= "percent"
	caret_key	= "asciicircum"
	and_key		= "ampersand"
	star_key	= "asterisk"
	left_bracket_key	= "braceleft"
	right_bracket_key	= "braceright"
	double_point_key	= "colon"
	point_key	= "period"
	comma_key	= "comma"

	def __init__(self):
		self.root = None
		
		self.lastPressKey = ""
		
	def pressKey(self):
		if self.root is None:
			self.root = tk.Tk()
			self.root.bind_all('<Key>', self.bindKey)
			#self.root.withdraw()
			self.root.mainloop()
		
		return self.lastPressKey
	
	def bindKey(self, event):
		c = event.char
		cc = event.keysym
		print "LAST", c, cc
		if c == self.escape:
			self.root.destroy()
		self.lastPressKey = (c,cc)
"""
km = KeyMap()
print "press any key (ESC - end)"
while True:	
	key_code = km.pressKey()
	if KeyMapper.escape == key_code:
		print "end"
		break
	print "key code:", key_code
#"""




"""
def keypress(event):
	print "PRESSED", event.keysym, "CHAR",  event.char
	if event.keysym == 'Escape':
		root.destroy()
	x = event.char
	if x == "w":
		print "blaw blaw blaw"
	elif x == "a":
		print "blaha blaha blaha"
	elif x == "s":
		print "blash blash blash"
	elif x == "d":
		print "blad blad blad"
	else:
		print "kuku"
	
root = tk.Tk()
print "Press a key (Escape key to exit):"
#frame = tk.Frame(root, width=100, height=100)
root.bind_all('<Key>', keypress)
# don't show the tk window
#frame.pack()
#root.withdraw()
root.mainloop()
"""
