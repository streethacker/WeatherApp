#!/usr/bin/env python
#-*- coding:utf-8 -*-

import xml.etree.ElementTree as ET
import StringIO
import gzip
import urllib

class OpenSourceError(IOError, OSError):
	"Self-designed Exception"
	pass

def UnifyInputSource(source):
	"""
	Unified the input source type so that no matter a file or file-like object, a local path, a url or even
	a string is given, only a file or file-linke object will be returned and then passed to the parser of
	xml.
	"""

	#already a file or file-like object, or a gzip.
	if hasattr(source, "read"):
			if hasattr(source, "headers"):
					encoding = source.headers.get("Content-Encoding")
					if encoding == "gzip":
							compressdata = StringIO.StringIO(source.read())
							gzipper = gzip.GzipFile(fileobj = compressdata)
							return StringIO.StringIO(gzipper.read())
			else:
					return source

	#if a local path is given
	try:
			return open(source, "rb")
	except OpenSourceError:
			pass

	#if a url is given
	try:
			return urllib.urlopen(source)
	except OpenSourceError:
			pass

	return StringIO.StringIO(str(source))

class XMLHandler:
	def __init__(self, target):
		self._unify = UnifyInputSource(target)
		self._xmltree = ET.parse(self._unify)
		self._root = self._xmltree.getroot()



if __name__ == "__main__":
		pass
