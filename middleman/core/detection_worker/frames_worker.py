#! /usr/bin/env python
# coding:utf-8

import sys
import cv2
import cv2.cv as cv	#for old code
from numpy import *

from rectangles_worker import RectanglesWorker

class FramesWorker:
	#frames = []
	
	def __init__(self, frames = []):
		"""
		Při inicializaci se může rovnou nahrat seznam framů s obdélníky jinak seznam bude prázdný.
		Jedná se o třídu pro práci s frámy. Obsahuje několik algoritmů.
		@param	frames	Seznam framů s detekčními obdélníky
		@param	rotation_rectangles	Zda se jedna o obdélníky, které mohou byt natočené (True) nebo statické jednoúhlové (False - default) [NOT IMPLEMENTED]
		"""
		self.frames = []
		# zda se jedná o list nebo numpy
		if type(frames) == type( [] ) or type(frames) == type( array( [] ) ):
			self.frames = frames
		
	def setFrames(self, frames = [] ):
		"""
		Nastavení nového seznamu obdélníků.
		@param	frames	Seznam frámů
		@param	rotation_rectangles	Zda se jedna o obdélníky, které mohou byt natočené (True) nebo statické jednoúhlové (False - default) [NOT IMPLEMENTED]
		"""
		if type(frames) == type( [] ) or type(frames) == type( array( [] ) ):
			self.frames = frames
	
	def getFrames(self):
		"""
		Vrácení aktuální sestavy frámů.
		@return	Aktuální sestava frámů
		"""
		return self.frames
		
	def getCount(self):
		"""
		Počet framů v seznamu/bufferu
		@return	počet framů
		"""
		return len(self.frames)
	
	
	def averagingAppropriateRectangles(self, size_divergence = 0.25, position_divergence = 0.25, mode_position = True, buble_mode = False):
		"""
		Zprůměrování podobných obdélníků na podobném místě v daném framů. Aplikuje se pro každý frame zvlášť
		@param	size_divergence	koeficient (procenta 1 = 100 %, 0.5 = 50 %, 0 = 0% [stejně velké] ) o kolik mohou být obdélníky rozdílné
		@param	posittion_divergence z největšího obdelník se převede na čtverec se stejným obvodem a ten se na základě tohoto koeficientu zvětší/zmenší. V tomto prostoru se musí nacházet střed druhého/menšího obdelníku
		@param	mode_position	zda se má určovat střed dle čtverce či kružnice
		@return	seznam frámu s pruměrovanými obdélníky
		"""
		new_frames = []
		rw = RectanglesWorker()
		for frame in self.frames:
			rw.setRectangles( frame )
			new_frames.append( rw.averagingAppropriateRectangles( size_divergence, position_divergence, mode_position, buble_mode ) )
		self.frames = new_frames
		return new_frames
	
	def filteringIncorrectRectangles(self, buffer_size, find_in_buffer, step_coefficient = 0.25, maximum_step = -1, size_divergence = 0.25, position_divergence = 0.25, mode_position = True):
		"""
		Algoritmus na odfiltrování ustřelených detekcí v hadovitém hledání
		@param	buffer_size	Velikost bufferu
		@param	find_in_buffer	Minimální počet framů ve kterých musí byt nalezené podobné detekce (maximální velikost: buffer_size - 1)
		@param	step_coefficient	O kolik se má v každém následujícím framu navýšit position_divergence pokud nebyla nalezená detekce v aktuální framu
		@param	maximum_step	Kolikrát se může navýšit position_divergence o step_coefficient (-1 - vypnuto - neomezeněkrát; 0 - nenavýšovat)
		@param	size_divergence	koeficient (procenta 1 = 100 %, 0.5 = 50 %, 0 = 0% [stejně velké] ) o kolik mohou být obdélníky rozdílné
		@param	posittion_divergence z největšího obdelník se převede na čtverec se stejným obvodem a ten se na základě tohoto koeficientu zvětší/zmenší. V tomto prostoru se musí nacházet střed druhého/menšího obdelníku
		@param	mode_position	zda se má určovat střed dle čtverce či kružnice
		
		@return	jeden frame
		"""
		# zjistíme zda je buffer velky jak je vyžadováno a pokud hodnota find_in_buffer je menší než velikost buffer_size
		if self.getCount() != buffer_size or find_in_buffer >= buffer_size or buffer_size <= 0:
			self.frames = [[]]
			return []
		
		# získání prvního framu s detekci
		i = 1
		for frame in self.frames:
			if len(frame) > 0:
				actual_frame = frame
				break;
			i += 1
		
		# zjištění zda má smysl dále provádět tento algoritmus
		if find_in_buffer > buffer_size - i:
			self.frames = [[]]
			return []
		
		# porovnání detekčních obdélníku z actual_frame s ostatními obdélníky ostatních framů
		rw = RectanglesWorker()
		filtered_frame = []
		for actual_rectangle in actual_frame:
			candidate_rectangle = actual_rectangle
			position_divergence_modification = position_divergence
			divergence_counter = 0
			find_counter = 0
			find = False
			# ostatní framy (bez zbytečných, které by jen zavazely a dělaly šum)
			for other_frame in self.frames[i:]:
				# obdélníky z tohoto framu
				for other_rectangle in other_frame:
					# porovnání actual_rectangle s other_rectangle
					params = {
						"rectangle_1"	: actual_rectangle,
						"rectangle_2"	: other_rectangle,
						"size_divergence"	: size_divergence,
						"position_divergence"	: position_divergence_modification,
						"mode_position"	: mode_position
					}
					if rw.compareRectangles( **params ):
						actual_rectangle = other_rectangle
						divergence_counter = 0
						position_divergence_modification = position_divergence
						# smazat other_rectangle v tomto framu? To je mi teda otázka :D
						find_counter += 1
						if find_counter == find_in_buffer:
							filtered_frame.append( candidate_rectangle )
							find = True
						break
					else:
						divergence_counter += 1
						if divergence_counter <= maximum_step or maximum_step < 0:
							position_divergence_modification += step_coefficient
				# nyní už je zbytečné prohledávat v dalších framech pokud je obdélník nalezený v daném počtu
				if find:
					break
		self.frames = [ filtered_frame ]
		return filtered_frame
	
	def keyRectangle(self, find_in_buffer, number_steps_predict, step_coefficient = 0.25, maximum_step = -1, size_divergence = 0.25, position_divergence = 0.25, mode_position = True):
		"""
		Algoritmus, který předá frame s jedním (nebo žádným) detekčním obdélníkem zájmu za pomoci hadovitého hledání
		@param	find_in_buffer	Minimální počet framů ve kterých musí byt nalezené podobné detekce (maximální velikost: buffer_size - 1)
		@param	number_steps_predict	Počet framů k vytvoření predikčního framu CDR (Candidates Detection Rectangles)
		@param	step_coefficient	O kolik se má v každém následujícím framu navýšit position_divergence pokud nebyla nalezená detekce v aktuální framu
		@param	maximum_step	Kolikrát se může navýšit position_divergence o step_coefficient (-1 - vypnuto - neomezeněkrát; 0 - nenavýšovat)
		@param	size_divergence	koeficient (procenta 1 = 100 %, 0.5 = 50 %, 0 = 0% [stejně velké] ) o kolik mohou být obdélníky rozdílné
		@param	posittion_divergence z největšího obdelník se převede na čtverec se stejným obvodem a ten se na základě tohoto koeficientu zvětší/zmenší. V tomto prostoru se musí nacházet střed druhého/menšího obdelníku
		@param	mode_position	zda se má určovat střed dle čtverce či kružnice
		
		@return	vyfiltrovaný frame s jedním nebo žádným detekčním obdélníkem zájmu
		"""
		# kontrola hodnot a zda buffer má minimální velikost
		if find_in_buffer < number_steps_predict + 1: 
			self.frames = [[]]
			return self.frames
		
		if number_steps_predict <= 1:
			self.frames = [[]]
			return self.frames
		
		if self.getCount() <= find_in_buffer:
			self.frames = [[]]
			return self.frames
		
		# Nalezení kandidátů (CDR - Candidates Detection Rectangles) v prvních framech (dle počtu number_steps_predict)
		cdr = []
		acdr = [] # ACDR - Actual Candidates Detection Rectangles
		#position_divergence_list = []
		#find_list = []
		rw = RectanglesWorker();
		i = 0
		for frame in self.frames:
			i += 1
			# ukončíme pokud je již přesahnutý počet NSP
			if i > number_steps_predict:
				break
			# je-li frame prázdný skočíme na další
			if len( frame ) == 0:
				continue
			# je-li CDR prázdné pak jej naplníme obdélníky z aktualního frámu
			if len( cdr ) == 0:
				cdr = frame[:]
				acdr = frame[:]
				continue
			# porovnáme obdélníky z aktuálního frámu s obdélníky v acdr
			tmp_acdr = acdr[:]
			r_i = 0
			for rectangle in frame:
				c_i = 0
				for candidate in tmp_acdr:
					# porovnání podobnosti rectangle a candidate
					params = {
						"rectangle_1"	: candidate,
						"rectangle_2"	: rectangle,
						"size_divergence"	: size_divergence,
						"position_divergence"	: position_divergence,
						"mode_position"	: mode_position
					}
					if rw.compareRectangles( **params ):
						# je-li odpověď kladná pak aktalizujeme candidate za rectangle
						acdr[ c_i ] = rectangle
						#position_divergence_list[ c_i ] = position_divergence
						#find_list[ c_i ] = True
					else:
						# je-li odpověď záporná pak přidáme rectangle do CDR i ACDR
						cdr.append( rectangle )
						acdr.append( rectangle )
						#position_divergence_list.append( position_divergence )
						#find_list.append( True )
					c_i += 1
				r_i += 1
		
		# promazání listů
		del acdr
		
		# je-li CDR prázdné ukončíme algoritmus
		if len( cdr ) == 0:
			self.frames = [[]]
			return self.frames
		
		# hadovité prohledávání seznamu a porovnávání kandidátů a zjišťování jejich hodnot
		
		# ověřujeme postupně všechny kandidáty
		candidate_price_list = []
		find_counter_list = []
		for candidate in cdr:
			# Actual Detection Rectangle
			adr = candidate
			candidate_price = 0
			actual_position = 0
			i = 0
			divergence_counter = 0
			find_counter = 0
			no_match = 0
			position_divergence_modiffication = position_divergence
			for frame in self.frames:
				actual_position += 1
				find = False
				# je-li frame prázdný skočíme na další
				if len( frame ) == 0:
					if divergence_counter <= maximum_step or maximum_step < 0:
						position_divergence_modiffication += step_coefficient
					continue
				# porovnáme s jednotlivými obdélníky v aktuálním framů
				for rectangle in frame:
					params = {
						"rectangle_1"	: adr,
						"rectangle_2"	: rectangle,
						"size_divergence"	: size_divergence,
						"position_divergence"	: position_divergence_modiffication,
						"mode_position"	: mode_position
					}
					if rw.compareRectangles( **params ):
						# jsou-li podobné tak ukončíme tento cyklus a aktualizujeme ADR
						adr = rectangle
						find_counter += 1
						candidate_price += ( find_counter + self.getCount() ) - ( actual_position + no_match )
						no_match = 0
						find = True
						position_divergence_modiffication = position_divergence
						break
				if find == False:
					# nejsou-li podobné žádné tak navyšíme position_divergence_modiffication a no_match
					if divergence_counter <= maximum_step or maximum_step < 0:
						position_divergence_modiffication += step_coefficient
					no_match += 1
			
			candidate_price -= no_match
			# zaevidování pro další použití
			candidate_price_list.append( candidate_price )
			find_counter_list.append( find_counter )
		# rozhodnutí z kterých kandidátu je nejvhodnější
		rectangle = cdr[ 0 ]
		candidate_price = candidate_price_list[ 0 ]
		find_counter = find_counter_list[ 0 ]
		for i in range( 1, len( cdr ) ):
			if candidate_price < candidate_price_list[ i ] and find_in_buffer < find_counter_list[ i ]:
				rectangle = cdr[ i ]
				candidate_price = candidate_price_list[ i ]
				find_counter = find_counter_list[ i ]
		
		if find_in_buffer < find_counter:
			self.frames = [[ rectangle ]]
		else:
			self.frames = [[]]
		return self.frames[0]
		
		
	def merging(self):
		"""
		Hloupé sloučení framů do jednoho framu. Zaevidovává však i do svého seznamu framů (s jedním frámem).
		@return jeden frame
		"""
		new_frame = []
		for frame in self.frames:
			for rectangle in frame:
				new_frame.append( rectangle )
		self.frames = [ new_frame ]
		return new_frame
	
	def mergingWithAveragingAppropriateRectangles(self, size_divergence = 0.25, position_divergence = 0.25, mode_position = True, buble_mode = True):
		"""
		Sloučení framů do jednoho framu, přičemž se podobné obdélníky budou průměrovat. Zaevidovává však i do svého seznamu framů (s jedním frámem).
		@retur	jeden frame
		"""
		self.merging()
		
		params = {
			"size_divergence"	: size_divergence,
			"position_divergence"	: position_divergence,
			"mode_position"	: mode_position,
			"buble_mode"	: buble_mode
		}
		self.averagingAppropriateRectangles( **params )
		return self.frames[0]
	
	
	
	
	
	
	
