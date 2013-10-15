#!/usr/bin/env python

import os
import urllib2

from autopkglib import Processor, ProcessorError

from Foundation import NSPredicate
import FoundationPlist

__all__ = ["CUDADriverURLProvider"]

CHECK_URL = 'https://partners.download.nvidia.com/activation/cuda_update_macos.xml'
PLIST_FN  = 'cuda_update_macos.plist'

class CUDADriverURLProvider(Processor):
	'''Provides URL to the latest CUDA Driver download from NVIDIA.'''

	input_variables = {
		'cuda_os_ver': {
			'required': False,
			'description': 'Version of OS to test the CUDA update NSPredicate with. Defaults to currently shipping Apple Mac OS X version.',
			},
	}
	output_variables = {
		'url': {
			'description': 'URL to the latest CUDA Driver DMG download'
		}
	}

	description = __doc__

	def get_url(self, os_ver):
		try:
			f = urllib2.urlopen(CHECK_URL)
			plist_text = f.read()
			f.close()
		except BaseException as e:
			raise ProcessorError('Could not retrieve check URL %s' % CHECK_URL)

		plist_filename = os.path.join(self.env['RECIPE_CACHE_DIR'], PLIST_FN)

		try:
			plistf = open(plist_filename, 'w')
			plistf.write(plist_text)
			plistf.close()
		except:
			raise ProcessorError('Could not write NVIDIA plist file %s' % plist_filename)

		try:
			plist = FoundationPlist.readPlist(plist_filename)
		except:
			raise ProcessorError('Could not read NVIDIA plist file %s' % plist_filename)

		# the Version is blank here due to the plist NSPredicate
		# testing it to not be the current version.
		pred_obj = {'Ticket': {'Version': ''}, 'SystemVersion': {'ProductVersion': os_ver}}

		for rule in plist['Rules']:
			try:
				predicate = NSPredicate.predicateWithFormat_(rule['Predicate'])
			except:
				raise ProcessorError('Problem with NSPredicate: %s' % rule['Predicate'])
	
			if predicate.evaluateWithObject_(pred_obj):
				return rule['Codebase']
			
		raise ProcessorError('No valid Predicate rules found!')

	def main(self):
		if 'cuda_os_ver' in self.env:
			cuda_os_ver = self.env['cuda_os_ver']
		else:
			cuda_os_ver = '10.8'

		self.env['url'] = self.get_url(cuda_os_ver)
		self.output('File URL %s' % self.env['url'])

if __name__ == '__main__':
	processor = CUDADriverURLProvider()
	processor.execute_shell()
