# encoding: utf-8

###########################################################################################################
#
#
#	General Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/General%20Plugin
#
#
###########################################################################################################

from __future__ import print_function
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from Foundation import NSFileManager
import os

class Backuper(GeneralPlugin):
	@objc.python_method
	def start(self):
		Glyphs.addCallback(self.doBackup_, DOCUMENTOPENED)

	def doBackup_(self, sender):
		document = sender.object()
		if document.fileURL() is None:
			return
		importedVersion = document.valueForKey_("importedVersion")
		if importedVersion != None and int(Glyphs.buildNumber) > int(importedVersion):
			documentPath = document.fileURL().path()
			fileName = os.path.basename(documentPath)
			bachupFolder = os.path.join(os.path.dirname(documentPath), "Backup")
			bachupPath = os.path.join(bachupFolder, importedVersion + "_" + fileName)
			
			fileManager = NSFileManager.defaultManager()
			if fileManager.fileExistsAtPath_isDirectory_(bachupFolder, None) == (False, False):
				if not fileManager.createDirectoryAtPath_withIntermediateDirectories_attributes_error_(bachupFolder, True, None, None):
					print("Could not make backup folder")
			
			if fileManager.isReadableFileAtPath_(documentPath):
				NSFileManager.defaultManager().copyItemAtPath_toPath_error_(documentPath, bachupPath, None)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
