#!/usr/bin/env python

from glob import glob
from autopkglib import Processor, ProcessorError

__all__ = ["GlobFileFinder"]

class GlobFileFinder(Processor):
	'''Finds a file that matches a glob in a directory.'''

	input_variables = {
		'glob_pattern': {
			'description': 'Glob pattern to match files by',
			'required': True,
		},
	}
	output_variables = {
		'glob_match': {
			'description': 'First matched glob file',
		}
	}

	description = __doc__

	def globfind(self, pattern):
		foundglob = glob(pattern)

		if len(foundglob) < 1:
			raise ProcessorError('No match')
		elif len(foundglob) > 1:
			raise ProcessorError('Too many matches')

		return foundglob[0]

	def main(self):
		pattern = self.env.get('glob_pattern')

		self.env['glob_match'] = self.globfind(pattern)

		if len(self.env['glob_match']) > 0:
			self.output('Found match %s' % self.env['glob_match'])

if __name__ == '__main__':
	processor = GlobFileFinder()
	processor.execute_shell()
