#!/usr/bin/env python
#-*- coding:utf-8 -*-

import xml.etree.ElementTree as ET

class XMLHandler:
	def __init__(self, source):
		self.tree = ET.parse(source)
		self.root = self.tree.getroot()

	def parse_jiangsu(self, pyName=None):
		self.status = {}
		if pyName:
				for city in self.root.findall("city"):
						if city.get("pyName") == pyName:
								self.status["cityName"] = city.get("cityName")
								self.status["stateDetailed"] = city.get("stateDetailed")
								self.status["temLow"] = city.get("tem2")
								self.status["temHigh"] = city.get"tem1")
								self.status["tmpNow"] = city.get("temNow")
								self.status["winState"] = city.get("winState")
								self.status["humanity"] = city.get("humanity")
								self.status["time"] = city.get("time")

								break

				return self.status
		else:
				extractMethod = lambda d: {k:v for k, v in d.items() if k in ["stateDetailed", "tem1", "tem2", "winState"]}
				for city in self.root.findall("city"):
						self.status[city.get("cityName")] = extractMethod(city.attrib)

				return self.status

	def parse_china(self, pyName=None):
		self.status = {}

		extractMethod = lambda d: {k:v for k, v in d.items() if k in ["quName","stateDetailed", "tem1", "tem2", "winState"]}
		if pyName in ["xisha", "nansha", "diaoyudao"]:
				for city in self.root.findall("city"):
						if city.get("pyName") == pyName:
								self.status["cityName"] = city.get("cityName")
								self.status["stateDetailed"] = city.get("stateDetailed")
								self.status["temLow"] = city.get("tem2")
								self.status["temHigh"] = city.get("tem1")
								self.status["winState"] = city.get("winState")

								break

				return self.status
		else:
				for city in self.root.findall("city"):
						self.status[city.get("cityName")] = extractMethod(city.attrib)

				return self.status

if __name__ == "__main__":
		pass
