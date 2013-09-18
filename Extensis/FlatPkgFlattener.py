import os
import shutil
import subprocess

from autopkglib import Processor, ProcessorError

__all__ = ["FlatPkgFlattener"]


class FlatPkgFlattener(Processor):
	'''Flatten an expanded package using pkgutil'''

	description = __doc__

	input_variables = {
		'source_pkg_dir': {
			'description': 'Path to an extracted flat package',
			'required': True,
		},
		'destination_pkg': {
			'description': 'Name of destination pkg to be flattened',
			'required': True,
		},
	}

	output_variables = {}

	def flatten(self, source_dir, dest_pkg):
		try:
			subprocess.check_call(['/usr/sbin/pkgutil', '--flatten', source_dir, dest_pkg])
		except subprocess.CalledProcessError, err:
			raise ProcessorError("%s flattening %s" % (err, source_dir))

	def main(self):
		source_dir = self.env.get('source_pkg_dir')
		dest_pkg = self.env.get('destination_pkg')

		self.flatten(source_dir, dest_pkg)

if __name__ == '__main__':
	processor = FlatPkgFlattener()
	processor.execute_shell()
