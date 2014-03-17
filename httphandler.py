#!/usr/bin/env python
#-*- coding:utf-8 -*-

import urllib2, urlparse, gzip

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 \
			Safari/537.36 SUSE/33.0.1750.117"

class SchemeFailure(Exception):
	"Self-designed Exception."
	pass

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
	"""
	Inherited from HTTPRedirectHandler, redefined the http_error_xxx method adding the 'status' attribute
	to the object(result) returned.
	"""
	def http_error_301(self, req, fp, code, msg, headers):
		result = urllib2.HTTPRedirectHandler.http_error_301(self, req, \
				fp, code, msg, headers)
		result.status = code
		return result

	def http_error_302(self, req, fp, code, msg, headers):
		result = urllib2.HTTPRedirectHandler.http_error_302(self, req, \
				fp, code, msg, headers)
		result.status = code
		return result

class DefaultErrorHandler(urllib2.HTTPDefaultErrorHandler):
	"""
	Inherited from DefaultErrorHandler, redefined the http_error_default method returning a HTTPError object
	and adding one new attribute -- status.
	"""
	def http_error_default(self, req, fp, code, msg, headers):
		result = urllib2.HTTPError(req.get_full_url(), code, msg, headers, fp)
		result.status = code
		return result


def OpenHTTPResource(target, etag=None, lastmodified=None, agent=USER_AGENT):
	"""
	Open the target url, with several headers added:
		User-Agent: default to USER_AGENT if not assigned;
		Accept-Encoding: default to 'gzip';
		If-None-Match: if etag is given;
		If-Modified-Since: if lastmodified is given.
	and return a HTTPResponse or HTTPError object. Maybe raise an Exception of SchemeFailure.
	"""
	if urlparse.urlparse(target)[0] == "http":
			request = urllib2.Request(target)
			request.add_header("User-Agent", agent)
			request.add_header("Accept-Encoding", "gzip")
			if etag:
					request.add_header("If-None-Match", etag)
			if lastmodified:
					request.add_header("If-Modified-Since", lastmodified)

			opener = urllib2.build_opener(SmartRedirectHandler(), DefaultErrorHandler())
			return opener.open(request)
	else:
			raise SchemeFailure, "Please ensure the scheme part of your url is 'http'."

if __name__ == "__main__":
		pass
