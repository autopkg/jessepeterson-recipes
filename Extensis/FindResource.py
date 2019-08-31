#!/usr/bin/env python

from __future__ import absolute_import
from autopkglib import Processor, ProcessorError
import os

__all__ = ["FindResource"]

class FindResource(Processor):
	'''Finds a file resource in the current rescipe directory, or any parent recipe directories'''

	input_variables = {
		'filename': {
			'required': True,
			'description': 'Name of filename resource',
		},
		'output_var_name': {
			'required': False,
			'description': 'Name of environment variable to output found file. Defaults to "found_resource"'
		},
	}
	output_variables = {
		'output_var_name': {
			'description': 'Name of environment variable to output found file. Defaults to "found_resource"'
		},
	}

	def main(self):
		filename = self.env.get('filename', None)

		output_var = self.env.get('output_var_name', 'found_resource')

		resource_file = os.path.join(self.env.get('RECIPE_DIR'), filename)
		if os.path.exists(resource_file):
			self.env[output_var] = resource_file
			self.output('Found resource in current recipe dir: %s' % resource_file)
			return

		for parent_recipe in self.env.get('PARENT_RECIPES', []):
			resource_file = os.path.join(os.path.dirname(parent_recipe), filename)

			if os.path.exists(resource_file):
				self.env[output_var] = resource_file
				self.output('Found resource in parent recipe dir: %s' % resource_file)
				return

		self.output('Could not find resource "%s" in recipe dir nor parent recipe dirs' % filename)
