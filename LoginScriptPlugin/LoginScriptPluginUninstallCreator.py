#!/usr/bin/python
#
# Copyright 2016 Jesse Peterson
#
#        DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.
#
"""See docstring for LoginScriptPluginUninstallCreator class"""

from __future__ import absolute_import

from autopkglib import Processor

__all__ = ["LoginScriptPluginUninstallCreator"]

SCRIPT_PREPEND = '''#!/bin/bash
# reset positional arguments so the script automatically disables the plugin
set -- disable
'''

class LoginScriptPluginUninstallCreator(Processor):
    '''Moves/renames a file'''

    input_variables = {
        'script_path': {
            'description': 'Script file to modify',
            'required': True,
        }
    }
    output_variables = {
    }

    description = __doc__

    def main(self):
        with open(self.env['script_path'], 'r') as f:
            filecontents = f.read()

        with open(self.env['script_path'], 'w') as f:
            f.write(SCRIPT_PREPEND + filecontents)

        self.output(
            'Modified %s script (%d bytes -> %d bytes)' % (self.env['script_path'], len(filecontents), len(SCRIPT_PREPEND + filecontents)))

if __name__ == '__main__':
    PROCESSOR = LoginScriptPluginUninstallCreator()
    PROCESSOR.execute_shell()
