#!/usr/bin/env python

import datetime
import re
import urllib2

from autopkglib import Processor, ProcessorError

__all__ = ["VirtualBoxURLProvider"]

ROOT_URL = 'http://download.virtualbox.org/virtualbox'
LATEST_URL = ROOT_URL + '/LATEST.TXT'

re_vbox = re.compile('(VirtualBox-[0-9\.]*-[0-9]*-OSX\.dmg)')
re_ext = re.compile('(Oracle_VM_VirtualBox_Extension_Pack-[0-9\.]*-[0-9]*\.vbox-extpack)')

class VirtualBoxURLProvider(Processor):
	'''Provides URL to the latest VirtualBox version.'''

	input_variables = {}
	output_variables = {
		'virtualbox_version': {
			'description': 'Version of VirtualBox release'
		},
		'virtualbox_url': {
			'description': 'URL to the latest Universal Type Client 3 download'
		},
		'extpack_url': {
			'description': 'URL to the latest Universal Type Client 3 download'
		},

	}

	description = __doc__

	def get_latest(self):
		try:
			f = urllib2.urlopen(LATEST_URL)
			latest = f.readline()
			f.close()
		except BaseException as e:
			raise ProcessorError('Could not retrieve URL: %s' % LATEST_URL)

		return latest.strip()

	def get_urls(self, latest):
		md5_url = '%s/%s/MD5SUMS' % (ROOT_URL, latest)

		try:
			f = urllib2.urlopen(md5_url)
			md5sums = f.read()
			f.close()
		except BaseException as e:
			raise ProcessorError('Could not retrieve URL: %s' % md5_url)

		m = re_vbox.search(md5sums)
		if m:
			vb_url = '/'.join((ROOT_URL, latest, m.group(1), ))
		else:
			raise ProcessorError('No matching VirtualBox software')

		m = re_ext.search(md5sums)
		if m:
			ext_url = '/'.join((ROOT_URL, latest, m.group(1), ))
		else:
			raise ProcessorError('No matching VirtualBox Ext. Pack software')

		return (vb_url, ext_url, )

	def main(self):
		self.env['virtualbox_version'] = self.get_latest()
		self.output('Latest is %s' % self.env['virtualbox_version'])

		vb_url, ext_url = self.get_urls(self.env['virtualbox_version'])

		self.env['virtualbox_url'] = vb_url
		self.env['extpack_url'] = ext_url

		self.output('VirtualBox URL: %s' % self.env['virtualbox_url'])
		self.output('Ext. pack  URL: %s' % self.env['extpack_url'])

if __name__ == '__main__':
	processor = VirtualBoxURLProvider()
	processor.execute_shell()
