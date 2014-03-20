#!/usr/bin/env python
#-*- coding:utf-8 -*-

__all__ = ["XMLHandler"]

import xml.etree.ElementTree as ET

class XMLHandler:
	def __init__(self, source):
		"""
		Accept a file or file-like object of xml, parse by ET(xml.etree.ElementTree) then
		get the root Element.
		"""
		self.tree = ET.parse(source)
		self.root = self.tree.getroot()

	def parse(self, pyName=None):
		"""
		The parse method plays an role of distributor, selecting the proper parse_xxx method
		by self-inspection.
		"""
		if self.root.tag == "china":
				parseMethod = getattr(self, "parse_china")
				return parseMethod(pyName)
		else:
				parseMethod = getattr(self, "parse_province")
				return parseMethod(pyName)

	def parse_province(self, pyName=None):
		"""
		If self.root.tag is not 'china', then this method will be excuted.
		If parameter pyName is given, a detailed weather report of specific city will be returned as a dictionary:
			{"cityname":cityname, "stateDetailed":stateDetailed, "temHigh":temHigh, "temLow":temLow, "temNow":temNow, \
			"windState":windState, "humidity":humidity, "time":time}

		Otherwise, a brief weather report of all the cities of the province will be returned as a folded dictionary: 
			{"cityname1":{state of the first city},
			"cityname2":{state of the second city},
			...
			"citynameX":{state of the Xth city}}
		"""
		self.status = {}
		if pyName:
				for city in self.root.findall("city"):
						if city.get("pyName") == pyName:
								self.status["cityname"] = city.get("cityname")
								self.status["stateDetailed"] = city.get("stateDetailed")
								self.status["temHigh"] = city.get("tem2")
								self.status["temLow"] = city.get("tem1")
								self.status["temNow"] = city.get("temNow")
								self.status["windState"] = city.get("windState")
								self.status["humidity"] = city.get("humidity")
								self.status["time"] = city.get("time")

								break

				return self.status
		else:
				extractMethod = lambda d: {k:v for k, v in d.items() if k in ["stateDetailed", "tem1", "tem2", "windState"]}
				for city in self.root.findall("city"):
						self.status[city.get("cityname")] = extractMethod(city.attrib)

				return self.status

	def parse_china(self, pyName=None):
		"""
		If self.root.tag is 'china', this method will be excuted.
		If pyName is given, it must within the range: ['xisha', 'nansha', 'diaoyudao'], then the weather report of the specific
		field will be returned as a dictionary:
			{"cityname":cityname, "stateDetailed":stateDetailed, "temHigh":temHigh, "temLow":temLow, "windState":windState}

		Otherwise a brief weather report of all the main cities of china will be returned as a folded dictionary:
			{"cityname1":{"quName1":quName1, the state of the city},
			"cityname2":{"quName2":quName2, the state of the city},
			...
			"citynameX":{"quNameX":quNameX, the state of the city}}
		"""
		self.status = {}

		extractMethod = lambda d: {k:v for k, v in d.items() if k in ["quName","stateDetailed", "tem1", "tem2", "windState"]}
		if pyName in ["xisha", "nansha", "diaoyudao"]:
				for city in self.root.findall("city"):
						if city.get("pyName") == pyName:
								self.status["cityname"] = city.get("cityname")
								self.status["stateDetailed"] = city.get("stateDetailed")
								self.status["temLow"] = city.get("tem2")
								self.status["temHigh"] = city.get("tem1")
								self.status["windState"] = city.get("windState")

								break

				return self.status
		else:
				for city in self.root.findall("city"):
						self.status[city.get("cityname")] = extractMethod(city.attrib)

				return self.status

if __name__ == "__main__":
		import urllib, StringIO, pprint
		data = urllib.urlopen("http://flash.weather.com.cn/wmaps/xml/jiangsu.xml")
		source = StringIO.StringIO(data.read())
		parser = XMLHandler(source)
		result = parser.parse()
		pprint.pprint(result)
