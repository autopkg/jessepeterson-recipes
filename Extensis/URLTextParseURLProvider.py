#!/usr/bin/env python

import datetime
import re
import urllib2

from autopkglib import Processor, ProcessorError

__all__ = ["URLTextParseURLProvider"]

class URLTextParseURLProvider(Processor):
	'''Provides URL to the latest UTC 3 version.'''

	input_variables = {
		're_pattern': {
			'description': 'Regular expression (Python) to match against page.',
			'required': True,
		},
		'url': {
			'description': 'URL of page to scrape',
			'required': True,
		},
	}
	output_variables = {
		'url': {
			'description': 'URL to the latest Universal Type Client 3 download'
		}
	}

	description = __doc__

	def get_url(self, url, re_pattern):
		try:
			f = urllib2.urlopen(url)
			content = f.read()
			f.close()
		except BaseException as e:
			raise ProcessorError('Could not retrieve URL: %s' % url)

		m = re_pattern.search(content)

		if m:
			return m.group(1)

		raise ProcessorError('No matched files')

	def main(self):
		re_pattern = re.compile(self.env['re_pattern'])
		self.env['url'] = self.get_url(self.env['url'], re_pattern)
		self.output('File URL %s' % self.env['url'])

if __name__ == '__main__':
	processor = URLTextParseURLProvider()
	processor.execute_shell()
