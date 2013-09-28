#!/usr/bin/env python

import datetime
import re
import urllib2

from autopkglib import Processor, ProcessorError

__all__ = ["UniversalTypeClient3URLProvider"]

file_pattern = re.compile('(UTC-3-[0-9\-]*-M.zip)', re.I)
DL_BASE = 'http://bin.extensis.com/'
DL_PAGE_URL = 'http://www.extensis.com/support/product-support/universal-type-server-3/'

class UniversalTypeClient3URLProvider(Processor):
	'''Provides URL to the latest UTC 3 version.'''

	input_variables = {}
	output_variables = {
		'url': {
			'description': 'URL to the latest Universal Type Client 3 download'
		}
	}

	description = __doc__

	def get_utc3_url(self):
		try:
			f = urllib2.urlopen(DL_PAGE_URL)
			html = f.read()
			f.close()
		except BaseException as e:
			raise ProcessorError('Could not retrieve HTML from %s' % flisturl)

		m = file_pattern.search(html)
		if m:
			return DL_BASE + m.group(1)
		else:
			raise ProcessorError('No matched files')

	def main(self):
		self.env['url'] = self.get_utc3_url()
		self.output('File URL %s' % self.env['url'])

if __name__ == '__main__':
	processor = UniversalTypeClient3URLProvider()
	processor.execute_shell()
