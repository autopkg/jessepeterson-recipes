import os
import shutil
import subprocess

from autopkglib import Processor, ProcessorError

__all__ = ["FlatPkgExpander"]


class FlatPkgExpander(Processor):
	'''Expand a flat package using pkgutil'''

	description = __doc__

	input_variables = {
		'flat_pkg_path': {
			'description': 'Path to a flat package',
			'required': True,
		},
		'destination_path': {
			'description': 'Directory where package will be unpacked; created if necessary',
			'required': True,
		},
	}

	output_variables = {}

	def expand(self, pkg_path, dest_dir):
		if os.path.isdir(dest_dir):
			try:
				shutil.rmtree(dest_dir)
			except (OSError, IOError), err:
				raise ProccessorError("Can't remove %s: %s" % (dest_dir, err))

		try:
			subprocess.check_call(['/usr/sbin/pkgutil', '--expand', pkg_path, dest_dir])
		except subprocess.CalledProcessError, err:
			raise ProcessorError("%s expanding %s" % (err, pkg_path))

	def main(self):
		pkg_path = self.env.get('flat_pkg_path')
		dest_dir = self.env.get('destination_path')

		self.expand(pkg_path, dest_dir)

if __name__ == '__main__':
	processor = FlatPkgExpander()
	processor.execute_shell()
