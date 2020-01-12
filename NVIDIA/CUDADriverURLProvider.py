#!/usr/bin/env python

from __future__ import absolute_import, print_function

import os
import subprocess

import FoundationPlist
from autopkglib import Processor, ProcessorError
from Foundation import NSPredicate

__all__ = ["CUDADriverURLProvider"]

CHECK_URL = 'https://partners.download.nvidia.com/activation/cuda_update_macos.xml'
PLIST_FN  = 'cuda_update_macos.plist'

class CUDADriverURLProvider(Processor):
    '''Provides URL to the latest CUDA Driver download from NVIDIA.'''

    input_variables = {
        'cuda_os_ver': {
            'required': False,
            'default': '10.14',
            'description': 'Version of OS to test the CUDA update '
                           'NSPredicate with. Defaults to 10.14.',
        },
    }
    output_variables = {
        'minimum_os_version': {
            'description': 'Minimum OS version requirement of the Driver DMG download.'
        },
        'version': {
            'description': 'Version of CUDA Driver DMG download.'
        },
        'url': {
            'description': 'URL to the latest CUDA Driver DMG download.'
        },
    }

    description = __doc__

    def evaluate_predicate(self, eval_obj, predicate_str):
        try:
            predicate = NSPredicate.predicateWithFormat_(predicate_str)
        except:
            raise ProcessorError('Problem with NSPredicate: %s' % predicate_str)
        return predicate.evaluateWithObject_(eval_obj)


    def get_url(self, os_ver):
        try:
            plist_text = subprocess.check_output(['/usr/bin/curl', '-s', '-1', CHECK_URL])
        except Exception as e:
            print(e)
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

        url = None
        version = None
        for rule in plist['Rules']:
            if self.evaluate_predicate(pred_obj, rule['Predicate']):
                self.output('Satisfied predicate for OS version %s' % os_ver)
                url = rule['Codebase']
                version = rule['kServerVersion']

                # with a satisfied predicate, evaluate lower OS versions
                # so as to determine a minimum OS constraint, decrementing
                # one 10.x version at a time
                while self.evaluate_predicate(pred_obj, rule['Predicate']):
                    # record the currently-evaluated OS version as the minimum required
                    minimum_os_ver = os_ver
                    osx, major = os_ver.split('.')
                    os_ver = osx + '.' + str(int(major) - 1)
                    pred_obj['SystemVersion']['ProductVersion'] = os_ver
                    self.output('Evaluating predicate for lower OS version %s' % os_ver)
                self.output('OS version %s too low!' % os_ver)
                # highest required versions seem to be always first, so we break
                # after we've satisfied one Predicate
                break


        if not url:
            raise ProcessorError('No valid Predicate rules found!')
        return (url, version, minimum_os_ver)

    def main(self):
        if 'cuda_os_ver' in self.env:
            cuda_os_ver = self.env['cuda_os_ver']
        else:
            cuda_os_ver = '10.10'

        self.env['url'], self.env['version'], self.env['minimum_os_version'] = self.get_url(cuda_os_ver)
        self.output('File URL %s, Version number %s' % (self.env['url'], self.env['version']))

if __name__ == '__main__':
    processor = CUDADriverURLProvider()
    processor.execute_shell()
