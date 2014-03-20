#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys, getopt
import StringIO
from httphandler import OpenHTTPResource
from xmlhandler import XMLHandler

URL_HEAD_CONST = "http://flash.weather.com.cn/wmaps/xml/"

PROVINCE_LIST = ["heilongjiang", "jilin", "liaoning", "hainan", "neimenggu", "xinjiang", "xizang", "qinghai", \
				"ningxia", "gansu", "hebei", "henan", "hubei", "hunan", "shandong", "jiangsu", "anhui", "shanxi" \
				"sanxi", "sichuan", "yunnan", "guizhou", "zhejiang", "fujian", "jiangxi", "guangdong", "guangxi", \
				"beijing", "tianjin", "shanghai", "chongqing", "xianggang", "aomen", "taiwan"]

class OutOfRangeException(Exception): pass

def InputUnified(source):
	if hasattr(source, "read"):
			if hasattr(source, "headers"):
					if source.headers.get("Content-Encoding"):
							import gzip

							compressdata = StringIO.StringIO(source.read())
							gzipper = gzip.GzipFile(fileobj=compressdata)
							return StringIO.StringIO(gzipper.read())
					else:
							return source

	try:
		return open(source, "r")
	except IOError, OSError:
		pass

	try:
		import urllib
		return urllib.urlopen(source)
	except IOError, OSError:
		pass

	return StringIO.StringIO(str(source))

def usage():
	document = \
	"""
	Brief introduction of how to use this module:
		if you want to get the information of the whole country(main cities):
				python main.py
		if you want to get the information of a certain province(main cities of this province):
				python main.py -F province_name or python main.py --field province_name
		if you want to get the information of a certain city of a certain province:
				python main.py -F province_name -c city_name or 
				python main.py --field province_name --city city_name
	NOTE: for some specifial fields namely ["xisha", "nansha", "diaoyudao"], you should specific the field as "china":
				python main.py -F china -c xisha or
				python main.py --field china --city xisha
	"""

	print document

def main(argv):
	try:
		opts, args = getopt.getopt(argv, "F:c:h", ["field=", "city=", "help"])
	except getopt.GetoptError as err:
		print "Error:", str(err)
		usage()
		sys.exit(1)

	opts_dict = {k:v for k, v in opts}

	if hasattr(opts_dict, "-h") or hasattr(opts_dict, "--help"):
			usage()
	elif hasattr(opts_dict, "-F") or hasattr(opts_dict, "--field"):
			field = opts_dict.get("-F") or opts_dict.get("--field")
			city = opts_dict.get("-c") or opts_dict.get("--city")
			if field == "china":
					target = URL_HEAD_CONST + "china.xml"
					urldata = OpenHTTPResource(target)
					source = InputUnified(urldata)
					parser = XMLHandler(source)
					parser.parse(city)
			elif field in PROVINCE_LIST:
					target = URL_HEAD_CONST + field + ".xml"
					urldata = OpenHTTPResource(target)
					source = InputUnified(urldata)
					parser = XMLHandler(source)
					parser.parse(city)
			else:
					raise OutOfRangeException, "Unsupported province of country name."
	else:
			target = URL_HEAD_CONST + "china.xml"
			urldata = OpenHTTPResource(target)
			source = InputUnified(urldata)
			parser = XMLHandler(source)
			parser.parse()


if __name__ == "__main__":
		main(sys.argv[1:])	
		
