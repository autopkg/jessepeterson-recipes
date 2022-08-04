#!/usr/local/autopkg/python

from __future__ import absolute_import

import os
import subprocess

from autopkglib import Processor, ProcessorError

__all__ = ["ImageConverter"]

class ImageConverter(Processor):
    '''Provides URL to the latest Darwin ISO of the VMware Fusion tools.'''

    input_variables = {
        'image_source': {
            'required': True,
            'description': 'Source image file',
            },
        'image_destination': {
            'required': True,
            'description': 'Output image file',
            },
        'image_format': {
            'required': True,
            'description': 'See hdiutil(1) manual for various image formats. E.g. UDTO',
            },
        'remove_destination': {
            'required': False,
            'description': 'Remove destination image file if it exists',
            },
    }
    output_variables = {
    }

    def main(self):
        if os.path.exists(self.env.get("image_destination")):
            if self.env.get("remove_destination", True):
                os.unlink(self.env.get("image_destination"))
            else:
                raise ProcessorError('image_destination exists')

        cmd = ['/usr/bin/hdiutil',
               'convert',
               self.env.get("image_source"),
               '-format',
               self.env.get("image_format"),
               '-o',
               self.env.get("image_destination"),
               ]

        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        proc.communicate()
        if proc.returncode != 0:
            raise ProcessorError('hdiutil convert exited abnormally')

        self.output("Converted %s to %s"
                     % (self.env["image_source"],
                        self.env["image_destination"]))


if __name__ == '__main__':
    processor = ImageConverter()
    processor.execute_shell()
