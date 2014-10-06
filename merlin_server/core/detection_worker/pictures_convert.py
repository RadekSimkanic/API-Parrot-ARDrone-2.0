#! /usr/bin/env python
# coding:utf-8

#zrychlení
#import psyco
#psyco.full()

import sys
import cv2
import cv2.cv as cv	#for old code


class PicturesConvert:
	"""
	Převod a vykreslení obrázků, detekce z obrázků
	"""
	xml_face		= "./xml/haarcascade_frontalface_alt.xml"
	xml_eye			= "./xml/haarcascade_eye.xml"
	xml_eye_glasses		= "./xml/haarcascade_eye_tree_eyeglasses.xml"
	xml_mouth		= "./xml/haarcascade_mcs_mouth.xml"
	xml_nose		= "./xml/haarcascade_mcs_nose.xml"
	xml_profile_face	= "./xml/haarcascade_profileface.xml"
	cascade_face		= cv2.CascadeClassifier(xml_face)
	cascade_eye		= cv2.CascadeClassifier(xml_eye)
	cascade_eye_glasses	= cv2.CascadeClassifier(xml_eye_glasses)
	cascade_mouth		= cv2.CascadeClassifier(xml_mouth)
	cascade_nose		= cv2.CascadeClassifier(xml_nose)
	cascade_profile_face	= cv2.CascadeClassifier(xml_profile_face)
	
	color_green		= (0, 255, 0)
	color_dark_green	= (0, 64, 0)
	color_red		= (0, 0, 255)
	color_dark_red		= (0, 0, 64)
	
	#image			= None
	#original_image		= None
	
	def __init__(self, image = None, scale = 1):
		"""
		Inicializace přijímá obrázek a případnou poměrovou změnu obrázku
		@param	image	obrázek
		@param	scale	změna velikosti obrázku
		"""
		if scale>1: 
			image = cv2.resize(image, (image.shape[1]/scale, image.shape[0]/scale) )
		# kontrola zda se jedná o numpy jinak None
		self.image = image
		self.original_image = image
	
	def resize(self, scale):
		"""
		Změna velikosti obrázku
		"""
		pass #self.image = cv2.resize(image, (image.shape[1]/scale, image.shape[0]/scale) )
	
	def getActualPicture(self):
		"""
		Vrátí aktuální obrázek se všemi úpravy
		"""
		return self.image
	
	def getOriginalActualPicture(self):
		"""
		Vrátí aktuální originální obrázek - bez jakýchkoliv aplikovaných úprav
		"""
		return self.original_image
		
	def setPicture(self, image):
		"""
		Nastaví jiný obrázek k zpracování (je brán jako originální)
		@param	image	obrázek
		"""
		# provést kontrolu
		self.image = image
		self.original_image = image
	
	def reset(self):
		"""
		Smaže veškeré změny provedené nad posledním vloženým obrázkem
		"""
		self.image = self.original_image
	
	def getGray(self):
		"""
		Převod obrázku do odstinu šedi
		@return	obrázek v odstinech šedi
		"""
		if self.image == None:
			return None
		self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
		return self.image
		
			
	def getGauss(self):
		"""
		Gausová filtrace včetně převodu do odstiu šedi
		@return	vyfiltrovaný obrázek
		"""
		if self.image == None:
			return None
		self.image = cv2.GaussianBlur(self.getGray(), (5,5),0)
		return self.image
			
	def getCanny(self, low_threshold=50, up_threshold=50):
		"""
		Cannyho hranový detektor, včetně převodu do odstínu šedi.
		@param	low_threshold	Velikost spodního prahu pro eliminaci nevýznamných hran. 
		@param	up_threshold	Velikost horního prahu pro eliminaci nevýznamných hran. 
		@return	vyfiltrovaný obrázek
		"""
		if self.image == None:
			return None
		self.image = cv2.Canny(self.getGauss(),	low_threshold,	up_threshold)
		return self.image
	
	def detection(self, cascade):
		"""
		Vlastní detekce
		@param	cascade	
		
		@return	seznam obdélníků se souřednicemi
		"""
		if self.image == None:
			return []
		rectangles = cascade.detectMultiScale(self.image, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
		if len(rectangles)==0:
			return []
		# [2:] - od indexu 2 po konec 
		# [:2] - od začátku po index 2 (ale ne včetně)
		rectangles[:,2:] += rectangles[:,:2]
		return rectangles
	
	def drawRectangles(self, rectangles, color = (0, 255, 0), border = 2):
		"""
		Vykreslení obdélníku do obrázku
		@param	rectangles	pole obdélniků
		@param	color	barva obdélniků
		@param	border šiřka čáry obdelníků
		
		@return	obrázek s vykreslenými obdelníky
		"""
		if self.image == None:
			return None
		
		if len(rectangles)==0 or len(rectangles[0]) != 4:
			return self.image
		for x1, y1, x2, y2 in rectangles:
			cv2.rectangle(self.image, (x1, y1), (x2, y2), color, border)
		return self.image
	
	def getFaceDetection(self):
		"""
		Detekce obličejů
		@return detekční obdélníky
		"""
		if self.image == None:
			return []
		
		rectangles	= self.detection(PicturesConvert.cascade_face )
		return rectangles
	
	def getEyeDetection(self):
		"""
		Detekce očí
		@return detekční obdélníky
		"""
		if self.image == None:
			return []
		rectangles	= self.detection(PicturesConvert.cascade_eye )
		return rectangles
		
	def getFaceAllDetection(self):
		"""
		Detekce obličejů, očí a brýli
		@return	detekční obdélníky
		"""
		if self.image == None:
			return []
		cascades	= [PicturesConvert.cascade_face, PicturesConvert.cascade_eye_glasses]
		rectangles	= getObjectsDetection()
		return rectangles
		
	
	def getObjectsDetection(self, cascades = []):
		"""
		Detekce podle seznamu "cascades"
		@param	cascades
		
		@return	detekční obdélníky
		"""
		if self.image == None:
			return []
		rectangles = []
		for cascade in cascades:
			rectangles.append(self.detection(cascade) )
		return rectangles
	
	def getPeopleDetection(self, win_stride = 8, padding = 32, scale = 1.15):#1.15	#1.05 jsem dosahl nejlepších detekcí | 1.15 dobrá a rychla detekce
		"""
		Detekce lidí za pomocí HOG Descriptoru z OpenCV
		@param	win_stride	Čtvercové rozdělení obrázku na síť stejně velkých bloků
		@param	padding	Rozměry detekčního okna
		@param	scale	Koeficient nárustu okna detekce
		
		@return	Vrátí souřadnice s detekcemi lidí
		"""
		if self.image == None:
			return []
		hog = cv2.HOGDescriptor()
		hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() ) 
				
		hog_params = {	"winStride"	: (win_stride,win_stride), #rozdělení obrázku na síť stejně velkých bloků (8 x 8 pixelů)
				"padding"	: (padding,padding), #default 32,32 # rozměry detekčního okna
				#"group_threshold":2,	# sloučení vícenásobných detekcí
				"scale"		: scale} # o kolik se má vstupní obrázek zvětšit; čim větší tim rychlejší ale horší detekce
		
		rectangles = hog.detectMultiScale(self.image, **hog_params)
		
		if len(rectangles)==0:
			return []
			
		print "před: ", rectangles, "konecPř"
		
		# předělání listu na souřadníce
		# [2:] - od indexu 2 po konec 
		# [:2] - od začátku po index 2 (ale ne včetně)
		#rectangles[:,2:] += rectangles[:,:2] 
		rectangles = self.sizesToCoordinates(rectangles)
		
		print "po: ", rectangles, "konecPo"
		
		return rectangles
		
	def sizesToCoordinates(self, rectangles):
		"""
		Změna na souřadnicové obdélníky. Z [x, y, w, h] se vytvoří [x, y, x2, y2]
		@param	rectangles	obdélníky (numpy nebo list)
		@return	souřadnicové obdélníky (list)
		"""
                new_r = []
                print "změna na souřadnice"
                for r in rectangles:
                        #print r
                        if len(r) != 4:
                                #print "continue"
                                continue
                        print r
                        x, y, w, h = r
                        new_r.append( [x, y, x+w, y+h] )
                return new_r
	
	def getPeopleDetectionRotation(self, win_stride = 8, padding = 32, scale = 1.15, number_rotation = 3, step_angle = 5):
		"""
		Detekce lidí za pomocí HOG Descriptoru z OpenCV. Několika násobná detekce nad jedním obrázkem v několika úhlech. Každé naklonění představuje jeden proces.
		@param	win_stride	Čtvercové rozdělení obrázku na síť stejně velkých bloků
		@param	padding	Rozměry detekčního okna
		@param	scale	Koeficient nárustu okna detekce
		@param	number_rotation	Počet natočení do obou směru po určitý úhel (step_angle)
		@param	step_angle	Úhel dle kterého se bude obraz natáčet pro detekci v každém kroku
		
		@return	Vrátí souřadnice s detekcemi lidí
		"""
		if self.image == None:
			return []
		#TODO
		#vytvořit pro každý proces/úhel novou instanci této tříde kde se provede natočení a následně detekce
		pass

	def rotation(self, angle, resize = True):
		"""
		Otočení obrázku
		@param	angle	Úhel o kolik se má obrázek natočit
		@param	resize	Zda se má obrázek zvětšovat v závislosti na natočení a tak přizpůsobovat velikost
		
		@return	natočený obrázek
		"""
		if self.image == None:
			return []
		#TODO
		pass


