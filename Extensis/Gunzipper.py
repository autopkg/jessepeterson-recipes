#!/usr/bin/env python

import subprocess
from autopkglib import Processor, ProcessorError

__all__ = ["Gunzipper"]

class Gunzipper(Processor):
	'''Gunzips a file'''

	description = __doc__

	input_variables = {
		"gzip_path": {
			"required": True,
			"description": "gzip file to gunzip"
		},
		"gunzip_path": {
			"required": True,
			"description": "gunzipped destination file",
		}
	}
	output_variables = {
	}

	def main(self):
		cmd = ['/usr/bin/gunzip', '-c', self.env.get("gzip_path")]

		try:
			gunzip_path_fh = open(self.env.get('gunzip_path'), 'wb')
			proc = subprocess.Popen(cmd,
			                        stdout=gunzip_path_fh,
			                        stderr=subprocess.PIPE)
			(_, stderr) = proc.communicate()
			gunzip_path_fh.close()
		except OSError as err:
			raise ProcessorError(
				"%s execution failed with error code %d: %s"
				% (os.path.basename(cmd[0]), err.errno, err.strerror))
		if proc.returncode != 0:
			raise ProcessorError(
				"Unarchiving %s with %s failed: %s"
				% (self.env.get("gzip_path", ""), os.path.basename(cmd[0]), stderr))
		else:
			self.output("Gunzipped %s" % self.env.get("gzip_path", ""))
			self.output("Gunzipped to %s" % self.env.get("gunzip_path", ""))

if __name__ == '__main__':
	processor = Gunzipper()
	processor.execute_shell()
