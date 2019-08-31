#!/usr/bin/env python

from __future__ import absolute_import
import datetime
import re
import urllib2

from autopkglib import Processor, ProcessorError

__all__ = ["VirtualBoxURLProvider"]

UPDATE_CHECK_URL = 'https://update.virtualbox.org/query.php?platform=DARWIN_64BITS_GENERIC&version=4.3.16_95972&count=97&branch=stable'
# While apparently not needed if the VBox folks start filtering by user agent
# here's an example from a running VirtualBox instance:
#   VirtualBox 4.3.16 <macosx.64 [Product: Darwiease: 13.4.0 | Version: Darwin Kernel Version 13.4.0: Sun Aug 17 19:50:11 PDT 2014; root:xnu-2422.115.4~1/RELEASE_X86_64]>
# See also https://github.com/autopkg/jessepeterson-recipes/issues/3

ROOT_URL = 'http://download.virtualbox.org/virtualbox'
LATEST_URL = ROOT_URL + '/LATEST.TXT'

re_vbox = re.compile('(VirtualBox-([0-9\.]*)-[0-9]*-OSX\.dmg)')
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

	def get_latest_file(self):
		try:
			f = urllib2.urlopen(LATEST_URL)
			latest = f.readline().rstrip()
			f.close()
		except BaseException as e:
			raise ProcessorError('Could not retrieve URL: %s' % LATEST_URL)

		# lame! use RE some day
		if '.' not in latest:
			raise ProcessorError('Not a valid VirtualBox version: %s' % latest)

		return latest

	def get_latest(self):
		'''Retrieve update check URL, parse, and return the current version
		number of the current VirtualBox. E.g. "4.23.16"

		The update check URL reply body seems to be one line with a version
		number and URL separated by a space character. In the first iteration
		of this Processor the first space-seperated parameter was the current
		version of VirtualBox. Somewhere in May 2015 this started returning
		a beta release number (5.0.0_BETA4) instead of the current version.
		So instead of using that first parameter attempt to parse out the
		version number from the second parameter which apparently is still
		the correct and current stable release URL.'''
		try:
			f = urllib2.urlopen(UPDATE_CHECK_URL)
			latest = f.readline()
			f.close()
		except BaseException as e:
			raise ProcessorError('Could not retrieve URL: %s' % LATEST_URL)

		upd_url = latest.split(' ', 1)[1]

		m = re_vbox.search(upd_url)
		if m:
			vb_ver = m.group(2)
		else:
			raise ProcessorError('No matching VirtualBox URL')

		return vb_ver

	def get_urls(self, version):
		md5_url = '/'.join((ROOT_URL, version, 'MD5SUMS', ))

		try:
			f = urllib2.urlopen(md5_url)
			md5sums = f.read()
			f.close()
		except BaseException as e:
			raise ProcessorError('Could not retrieve URL: %s' % md5_url)

		m = re_vbox.search(md5sums)
		if m:
			vb_url = '/'.join((ROOT_URL, version, m.group(1), ))
		else:
			raise ProcessorError('No matching VirtualBox software')

		m = re_ext.search(md5sums)
		if m:
			ext_url = '/'.join((ROOT_URL, version, m.group(1), ))
		else:
			raise ProcessorError('No matching VirtualBox Ext. Pack software')

		return (vb_url, ext_url, )

	def main(self):
		self.env['virtualbox_version'] = self.get_latest_file()
		self.output('Latest is %s' % self.env['virtualbox_version'])

		self.env['virtualbox_url'], self.env['extpack_url'] = \
			self.get_urls(self.env['virtualbox_version'])

		self.output('VirtualBox URL: %s' % self.env['virtualbox_url'])
		self.output('Ext. pack  URL: %s' % self.env['extpack_url'])

if __name__ == '__main__':
	processor = VirtualBoxURLProvider()
	processor.execute_shell()
