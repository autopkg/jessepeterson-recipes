#!/usr/bin/env python

import re
import urllib2

from autopkglib import Processor, ProcessorError

__all__ = ["CUDADriverURLProvider"]

CHECK_URL = 'http://www.nvidia.com/object/cuda-mac-driver.html'
BASE_DL_URL = 'http://us.download.nvidia.com'

re_dl = re.compile('confirmation\.php\?url\=(.*)\&lang')

class CUDADriverURLProvider(Processor):
	'''Provides URL to the latest CUDA Driver download from NVIDIA.'''

	input_variables = {
		'base_url': {
			'required': False,
			'description': 'Base Download URL for DMGs',
			},
	}
	output_variables = {
		'url': {
			'description': 'URL to the latest CUDA Driver DMG download'
		}
	}

	description = __doc__

	def get_url(self, base_url):
		try:
			f = urllib2.urlopen(CHECK_URL)
			html = f.read()
			f.close()
		except BaseException as e:
			raise ProcessorError('Could not retrieve check URL %s' % CHECK_URL)

		m = re_dl.search(html)

		if not m:
			raise ProcessorError('Could not find (match) latest version in check URL!')

		return base_url + m.group(1)

	def main(self):
		# Determine base_url.
		if "base_url" in self.env:
			base_url = self.env.base_url
		else:
			base_url = BASE_DL_URL

		self.env['url'] = self.get_url(base_url)
		self.output('File URL %s' % self.env['url'])

if __name__ == '__main__':
	processor = CUDADriverURLProvider()
	processor.execute_shell()
