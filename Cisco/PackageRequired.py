#!/usr/bin/env python

from autopkglib import Processor, ProcessorError
import os

__all__ = ["PackageRequired"]

class PackageRequired(Processor):
	'''Raises a ProcessorError if the PKG variable doesn't exist'''

	input_variables = {
	}
	output_variables = {
	}

	def main(self):
		pkg = self.env.get('PKG', None)

		if not pkg:
			raise ProcessorError('This recipe requires a package or disk '
			    'image to be pre-downloaded and supplied to autopkg ("-p" '
			    'option). This is likely due to a login being required to '
			    'download the software.')

		if not os.path.exists(pkg):
			raise ProcessorError('Path to package or disk image does not exist: %s' % pkg)
