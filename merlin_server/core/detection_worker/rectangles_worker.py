#! /usr/bin/env python
# coding:utf-8

import sys
import cv2
import cv2.cv as cv	#for old code
from numpy import *

#TODO udělat duplicitní třídu která bude počítat s rotací obdélníků a tuto třídu přejmenovat na SimpleRectangleWorker
class RectanglesWorker:
	#rectangles = []
	
	def __init__(self, rectangles = [] ):
		"""
		Při inicializaci se může rovnou nahrat seznam obdélníků jinak seznam bude prázdný.
		Jedná se o třídu pro práci s obdélníky. Obsahuje několik algoritmů.
		@param	rectangles	Seznam obdélníků
		@param	rotation_rectangles	Zda se jedna o obdélníky, které mohou byt natočené (True) nebo statické jednoúhlové (False - default)
		"""
		self.rectangles = []
		# zda se jedná o list nebo numpy
		if type(rectangles) == type( [] ) or type(rectangles) == type( array( [] ) ):
			self.rectangles = rectangles
	
	def setRectangles(self, rectangles = [] ):
		"""
		Nastavení nového seznamu obdélníků.
		@param	rectangles	Seznam obdélníků
		@param	rotation_rectangles	Zda se jedna o obdélníky, které mohou byt natočené (True) nebo statické jednoúhlové (False - default)
		"""
		if type(rectangles) == type( [] ) or type(rectangles) == type( array( [] ) ):
			self.rectangles = rectangles
	
	def getRectangles(self):
		"""
		Vrácení aktuální sestavy obdélníků.
		@return	Aktuální sestava obdélníků
		"""
		return self.rectangles
	
	
	def correctionRectangles(self, width = 0.75, height = 0.75):
		"""
		Změna rozměrů detekčních obdélníků
		@param width	šířka - je-li None nebo 0, nebude se měnit. Default: 0.75
		@param height	výška - je-li None nebo 0, nebude se měnit. Default: 0.75
		
		@return	přegenerované velikosti obdélníků
		"""
		if width in (None, 0):
			width = 1
		if height in (None, 0):
			height = 1
		width = 1 - width
		height = 1 - height
		new_rectangles = []
		for rectangle in self.rectangles:
			if len(rectangle) != 4:
				continue
			x1, y1, x2, y2 = rectangle
			width_corection = ( (x2 - x1) * float(width) ) / 2.0
			height_corection = ( (y2 - y1) * float(height) ) / 2.0
			x1 += int( round( width_corection ) )
			x2 -= int( round( width_corection ) )
			y1 += int( round( height_corection ) )
			y2 -= int( round( height_corection ) )
			new_rectangles.append([x1, y1, x2, y2])
		
		self.rectangles = new_rectangles
		return new_rectangles
		
	def getFindMaxWidthRectangle(self):
		"""
		Najde nejširší obdelník
		@return	Vrátí nejširší obdelník
		"""
		rectangle = []
		rectangle_width = 0
		
		for  rectangle in self.rectangles:
			if len(rectangle) != 4:
				continue
			x1, y1, x2, y2 = rectangle
			width = x2 - x1
			if rectangle_width < width:
				rectangle_width = width
				rectangle = [x1, y1, x2, y2]
		return rectangle
	
	def getWidthRectangle(self, rectangle):
		"""
		Šířka jednoho obdelníku, není-li žádný vráti 0
		@param	rectangle	obdélník
		
		@return	šířka obdelníku
		"""
		if len(rectangle) != 4 or rectangle == None:
			return 0
		else:
			x1, y1, x2, y2 = rectangle
			return x2 - x1	
	
	
	def getHeightRectangle(self, rectangle):
		"""
		Výška jednoho obdelníku, není-li žádný vráti 0
		@param	rectangle	obdélník
		
		@return	výška obdelníku
		"""
		if len(rectangle) != 4 or rectangle == None:
			return 0
		else:
			x1, y1, x2, y2 = rectangle
			return y2 - y1	
	
	
	def getFilteredMaxSizeRectangles(self, width = None, height = None):
		"""
		Vyfiltrování obdelníků, které přesahuji zadanou šířku nebo výšku
		@param	width	maximální šířka obdelníku (bude-li None - nebude se brát v potaz)
		@param	height	maximální výška obdelníku (bude-li None - nebude se brát v potaz)
		
		@return	obdélníky přesahující šířku nebo výšku
		"""
		new_rectangles = []
		if (width == None and height == None) or len(self.rectangles) == 0:
			return new_rectangles
		
		for rectangle in self.rectangles:
			if len(rectangle) != 4:
				continue
			x1, y1, x2, y2 = rectangle
			if width != None and x2 - x1 > width:
				new_rectangles.append([x1, y1, x2, y2])
			if height != None and y2 - y1 > height:
				new_rectangles.append([x1, y1, x2, y2])
		self.rectangles = new_rectangles
		return new_rectangles
	
	def compareRectangles(self, rectangle_1, rectangle_2, size_divergence = 0.25, position_divergence = 0.25, mode_position = True):
		"""
		Porovnání zda jsou oba obdélníky na podobném místě v podobné velikosti
		@param	rectangle_1	obdélník k porovnání
		@param	rectangle_2	obdélník k porovnání
		@param	size_divergence	koeficient (procenta 1 = 100 %, 0.5 = 50 %, 0 = 0% [stejně velké] ) o kolik mohou být obdélníky rozdílné
		@param	posittion_divergence z největšího obdélníku se převede na čtverec se stejným obvodem a ten se na základě tohoto koeficientu zvětší/zmenší. V tomto prostoru se musí nacházet střed druhého/menšího obdelníku
		@param	mode_position	zda se má určovat střed dle čtverce či kružnice (true - čtverec; false - kružnice)
		
		@return true | false
		"""
		if len(rectangle_1) != 4 or len(rectangle_2) != 4:
			return False
		
		if size_divergence > 1:
			size_divergence = 1
		if size_divergence < 0:
			size_divergence = 0
		if position_divergence < 0:
			position_divergence = 0
		
		x1r1, y1r1, x2r1, y2r1 = rectangle_1
		x1r2, y1r2, x2r2, y2r2 = rectangle_2
		
		# porovnání velikosti
		width1 = x2r1 - x1r1
		width2 = x2r2 - x1r2
		height1 = y2r1 - y1r1
		height2 = y2r2 - y1r2
		
		if width1 < width2:
			if width1 * (1+size_divergence) < width2: 
				return False
		else:
			if width2 * (1+size_divergence) < width1: 
				return False
		
		if height1 < height2:
			if height1 * (1+size_divergence) < height2: 
				return False
		else:
			if height2 * (1+size_divergence) < height1: 
				return False
		
		# středy obdélníků
		center_x_r1 = int( round( x1r1 + width1 / 2 ) )
		center_x_r2 = int( round( x1r2 + width2 / 2 ) )
		center_y_r1 = int( round( y1r1 + height1 / 2 ) )
		center_y_r2 = int( round( y1r2 + height2 / 2 ) )
		
		# půl obvod obdélníků
		half_perimeter_r1 = width1 + height1
		half_perimeter_r2 = width2 + height2
		
		# porovnání na základě čtverce nebo kružnice
		if mode_position:
			# porovnání umístění na základě přetransformování na čtverec a změny velikosti
			if half_perimeter_r2 > half_perimeter_r1:
				width = ( half_perimeter_r2 / 2 ) * position_divergence
				x1 = int( round( center_x_r2 - width / 2 ) )
				y1 = int( round( center_y_r2 - width / 2 ) )
				x2 = int( round( center_x_r2 + width / 2 ) )
				y2 = int( round( center_y_r2 + width / 2 ) )
				if x1 > center_x_r1 or x2 < center_x_r1 or y1 > center_y_r1 or y2 < center_y_r1:
					return False
			else:
				width = ( half_perimeter_r1 / 2 ) * position_divergence
				x1 = int( round( center_x_r1 - width / 2 ) )
				y1 = int( round( center_y_r1 - width / 2 ) )
				x2 = int( round( center_x_r1 + width / 2 ) )
				y2 = int( round( center_y_r1 + width / 2 ) )
				if x1 > center_x_r2 or x2 < center_x_r2 or y1 > center_y_r2 or y2 < center_y_r2:
					return False
		else:
			# porovnání umístění na základě přetransformování na kružnici a změny velikosti
			
			# zjištění velikost poloměru z obvodu
			if half_perimeter_r2 > half_perimeter_r1:
				r = half_perimeter_r2 / pi
			else:
				r = half_perimeter_r1 / pi
			r *= position_divergence
			# vzdalenost středu obdelníků
			distance = sqrt( square( center_x_r1 - center_x_r2 ) + square( center_y_r1 - center_y_r2 ) )
			if distance > r:
				return False
			
		return True
		
	def averagingRectangles(self):
		"""
		Vytvoření jednoho obdélníků na základě seznamu obdélníků
		@return zprůměrováný obdélník
		"""
		sumX1 = 0
		sumX2 = 0
		sumY1 = 0
		sumY2 = 0
		count = len( self.rectangles )
		for x1, y1, x2, y2 in self.rectangles:
			sumX1 += x1
			sumX2 += x2
			sumY1 += y1
			sumY2 += y2
		x1 = int( round( sumX1 / count ) )
		x2 = int( round( sumX2 / count ) )
		y1 = int( round( sumY1 / count ) )
		y2 = int( round( sumY2 / count ) )
		return [x1, y1, x2, y2]
		
	def averagingAppropriateRectangles(self, size_divergence = 0.25, position_divergence = 0.25, mode_position = True, buble_mode = False):
		"""
		Zprůměrování podobných obdélníků na podobném místě v daném framů. Aplikuje se pro každý frame zvlášť (seznam obdélníků je jeden frame)
		@param	size_divergence	koeficient (procenta 1 = 100 %, 0.5 = 50 %, 0 = 0% [stejně velké] ) o kolik mohou být obdélníky rozdílné
		@param	posittion_divergence z největšího obdelník se převede na čtverec se stejným obvodem a ten se na základě tohoto koeficientu zvětší/zmenší. V tomto prostoru se musí nacházet střed druhého/menšího obdelníku
		@param	mode_position	zda se má určovat střed dle čtverce či kružnice
		@param	buble_mode	je-li zapnut bublinkovy mod tak se provádí ověřování obdélníků do té doby dokud je vždy nějaký podobný obdélník nalezen. Je-li vypnut, provede se jen jednou.
		"""
		new_rectangles = []
		
		if buble_mode:
			# BUBLE mode
			rectangles = self.rectangles
			rw = RectanglesWorker()
			while True:
				i = 0
				find = False
				tmp_new_rectangles = []
				indexes_find_rectangles = []
				find_rectangles = []
				for rectangle in rectangles:
					tmp_new_rectangles = []
					i += 1
					j = 0
					find_rectangles = []
					indexes_find_rectangles = []
					indexes_find_rectangles.append(i)
					find_rectangles.append(rectangle)
					for rectangle_2 in rectangles:
						j += 1
						if j in indexes_find_rectangles:
							continue
						params = {
							"rectangle_1"	: rectangle,
							"rectangle_2"	: rectangle_2,
							"size_divergence"	: size_divergence,
							"position_divergence"	: position_divergence,
							"mode_position"	: mode_position
						}
						if self.compareRectangles( **params ):
							indexes_find_rectangles.append( j )
							find_rectangles.append( rectangle_2 )
							find = True
					if find:
						rw.setRectangles( find_rectangles )
						tmp_new_rectangles.append( rw.averagingRectangles() )
					else:
						tmp_new_rectangles.append(rectangle)
					
				#new_rectangles = tmp_new_rectangles
				rectangles = tmp_new_rectangles
				if find == False:
					new_rectangles = tmp_new_rectangles
					break
		else:
			# Clasic mode
			i = 0
			# pozice nalezených shodných obdélníků
			indexes_find_rectangles = []
			for rectangle in self.rectangles:
				i += 1
				j = i
				# list obdélníků pro zprůměrování
				find_rectangles = [rectangle]
				# nebudeme již testovat ty které již byly testované v předchozích iteracích
				for rectangle_2 in self.rectangles[i:]:
					# když je více shodných nálezu u vnějšího cyklus vnitřním cyklem pak tímto vynechat sparování s jinými obdélníky
					if j in indexes_find_rectangles:
						continue
					
					params = {
						"rectangle_1"	: rectangle,
						"rectangle_2"	: rectangle_2,
						"size_divergence"	: size_divergence,
						"position_divergence"	: position_divergence,
						"mode_position"	: mode_position
					}
					# ověříme zda jsou si obdélniky podobné
					if self.compareRectangles( **params ):
						indexes_find_rectangles.append( j )
						find_rectangles.append( rectangle_2 )
					j += 1
				# jsou-li nějaké nálezy pak je zpruměrujeme, jinak zaevidujeme nezpruměrovaný obdélník
				if len( find_rectangles ) > 1:
					rw = RectanglesWorker( find_rectangles )
					new_rectangles.append( rw.averagingRectangles() )
				else:
					new_rectangles.append( rectangle )
		
		self.rectangles = new_rectangles
		return self.filterEmptyRectangles()
	
	def filterEmptyRectangles(self):
		"""
		Smazat prázdné obdélníky bez souřadnic (smazat prázdné listy)
		"""
		new_rectangles = []
		for rectangle in self.rectangles:
			if len( rectangle ) != 4:
				continue
			new_rectangles.append( rectangle )
		self.rectangles = new_rectangles
		return new_rectangles
	
	
	
	
