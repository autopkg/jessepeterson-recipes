#!/usr/bin/env python

import urllib2
from autopkglib import Processor, ProcessorError

__all__ = ["FileZillaURLProvider"]

BASE_URL = 'https://update.filezilla-project.org/updatecheck.php'
BASE_URL += '?platform=i686-apple-darwin9&version=3.6.0.2'

class FileZillaURLProvider(Processor):
	"""Provides a download URL for the latest FileZilla release."""

	input_variables = {
		"base_url": {
			"required": False,
			"description": "Default is %s" % BASE_URL,
		},
	}

	output_variables = {
		"url": {
			"description": "URL to the latest FileZilla release.",
		},
	}

	description = __doc__

	def get_filezilla_apptbz_url(self, base_url):

		try:
			f = urllib2.urlopen(base_url)
			releasetext = f.read()
			f.close()
		except BaseException as err:
			raise ProcessorError("Can't download %s: %s" % (base_url, err))

		# parse FileZilla's proprietary release feed
		# it seems just a text file split by lines and further by
		# whitespace for each line
		for relline in releasetext.splitlines():
			splrelline = relline.split()
			if splrelline[0] == 'release':
				return splrelline[2]

		raise ProcessorError('No release branch!')

	def main(self):
		"""Find and return a download URL"""
		base_url = self.env.get("base_url", BASE_URL)
		self.env["url"] = self.get_filezilla_apptbz_url(base_url)
		self.output("Found URL %s" % self.env["url"])

if __name__ == "__main__":
	processor = FileZillaURLProvider()
	processor.execute_shell()
