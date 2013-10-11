#!/usr/bin/env python

import re
import urllib
import urllib2

from autopkglib import Processor, ProcessorError

__all__ = ["TrueCryptURLProvider"]

DLV_URL = 'http://www.truecrypt.org/downloads'
DLS_URL = 'http://www.truecrypt.org/dl'
re_verfind = re.compile('<input type="hidden" name="DownloadVersion" value="([0-9A-Za-z\.]*)">')

class TrueCryptURLProvider(Processor):
	'''Provides URL to the latest TrueCrypt installer DMG.'''

	input_variables = {
	}
	output_variables = {
		'url': {
			'description': 'URL to the latest download'
		}
	}

	description = __doc__

	def get_version(self):
		try:
			f = urllib2.urlopen(DLV_URL)
			content = f.read()
			f.close()
		except BaseException as e:
			raise ProcessorError('Could not retrieve URL: %s' % DLV_URL)

		m = re_verfind.search(content)

		if m:
			return m.group(1)

		raise ProcessorError('No version found')

	def get_url(self, version):
		'''Get the URL of the TrueCrypt DMG

		The TrueCrypt website has an HTML form that, when POSTed, returns
		a 302 redirect to the actual DMG download. Handle all of that, as
		ugly as it is, using urllib2.
		'''

		# no easy way to *not* follow redirects with urllib2, so do this
		class NoRedirectHandler(urllib2.HTTPRedirectHandler):
			def redirect_request(self, req, fp, code, msg, hdrs, newurl):
				pass

		submit_form = {
			'DownloadVersion': version,
			'MacOSXDownload': 'Download',
		}

		try:
			req = urllib2.Request(DLS_URL, urllib.urlencode(submit_form))

			opener = urllib2.build_opener(NoRedirectHandler)

			f = opener.open(req)
			content = f.read()
			f.close()
		except BaseException as e:
			if isinstance(e, urllib2.HTTPError) and e.code == 302:
				url = e.headers['Location']
			else:
				raise ProcessorError('Could not retrieve URL: %s' % DLS_URL)

		url_split = url.split('/')

		new_url = '/'.join(url_split[0:3]) + '/'
		new_url += urllib.pathname2url('/'.join(url_split[3:]))

		return new_url


	def main(self):
		tc_ver = self.get_version()
		self.output('Version: %s' % tc_ver)

		self.env['url'] = self.get_url(tc_ver)
		self.output('URL: %s' % self.env['url'])

if __name__ == '__main__':
	processor = TrueCryptURLProvider()
	processor.execute_shell()
