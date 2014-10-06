#! /usr/bin/env python
# coding:utf-8

import sys
import cv2
import cv2.cv as cv	#for old code


class HybridRingBuffer:
	size_buffer = 10
	data = []
	
	def __init__(self, size = None):
		"""
		@param	size	velikost kruhového bufferu
		"""
		if size != None:
			self.size_buffer = size
		self.data = []
	def add(self, item):
		"""
		Přidání dalšího prvku do bufferu
		@param	item	přidávaný prvek
		"""
		if len( self.data ) >= self.size_buffer:
			self.data.pop(0)
		self.data.append(item)
	
	def getAllItems(self):
		"""
		Vrátí obsah (list) celého bufferu
		@return	obsah jako list
		"""
		return self.data[::-1]
	
	def getFirstItem(self):
		"""
		Vrátí nejaktuálnější/nejčerstvější záznam
		@return záznam z kruhového bufferu
		"""
		if len( self.data ) == 0:
			return None
		return self.data[ len( self.data )-1]
	
	def getSecondItem(self):
		"""
		Vrátí druhý nejčerstvější záznam
		@return záznam z kruhového bufferu
		"""
		if len( self.data ) <=1:
			return None
		return self.data[ len( self.data )-2]
		
	def getLastItem(self):
		"""
		Vrátí nejstarší záznam
		@return	záznam z kruhového bufferu
		"""
		if len( self.data ) == 0:
			return None
		return self.data[0]
		
	def getItemInPosition(self, i):
		"""
		Vrátí záznam na dané pozici v bufferu
		@param	i	pozice v bufferu kde 0 je nejčerstvější záznam
		@raturn	záznam z kruhového bufferu
		"""
		if len(self.data) <= i:
			return None
		return self.data[ len( self.data )-i-1]
		
	def getSize(self):
		"""
		Aktuální velikost bufferu
		@return velikost
		"""
		return len( self.data )
