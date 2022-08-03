#!/usr/local/autopkg/python

#!/usr/bin/env python

from __future__ import absolute_import

from time import time

from autopkglib import Processor, ProcessorError

__all__ = ["TimestampVersioner"]

class TimestampVersioner(Processor):
    '''Returns a version of the current'''

    input_variables = {
        'version_major': {
            'description': 'Major component of version',
            'required': False,
        }
    }
    output_variables = {
        'version': {
            'description': 'Pseudo-version of the format <maj>.<min>. Maj is default 0 and min is the current epoch time.'
        },
    }

    description = __doc__

    def main(self):
        vmaj = self.env.get('version_major', '0')
        vmin = int(time())

        version = '%s.%d' % (vmaj, vmin)

        self.output('Version is %s' % version)

        self.env['version'] = version

if __name__ == '__main__':
    processor = TimestampVersioner()
    processor.execute_shell()
