#!/usr/bin/env python
#-*- coding:utf-8 -*-

import xml.etree.ElementTree as ET

class XMLHandler:
	def __init__(self, source):
		self.tree = ET.parse(source)
		self.root = self.tree.getroot()

	


if __name__ == "__main__":
		pass
