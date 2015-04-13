#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Tests for the `license context` function
"""

import unittest

from click.testing import CliRunner

from choosealicense.main import (context, LICENSE_WITH_CONTEXT,
                                 get_default_context)


class TestContext(unittest.TestCase):
    def test_show_license_context(self):
        all_the_licenses = (
            'agpl-3.0, apache-2.0, artistic-2.0, bsd-2-clause, '
            'bsd-3-clause, cc0-1.0, epl-1.0, gpl-2.0, gpl-3.0, '
            'isc, lgpl-2.1, lgpl-3.0, mit, mpl-2.0, unlicense')
        runner = CliRunner()
        for license in all_the_licenses.split(', '):
            result = runner.invoke(context, [license])
            output, exit_code = result.output, result.exit_code
            self.assertEqual(exit_code, 0)
            if license not in LICENSE_WITH_CONTEXT:
                self.assertEqual(output, ("Just use it, there's no context "
                                          "for the license.\n"))
            else:
                defaults = get_default_context()

                if license in ['mit', 'artistic-2.0', 'bsd-2-clause']:
                    self.assertEqual(
                        output,
                        ("The template has following defaults:\n"
                         "\tyear: {0}\n"
                         "\tfullname: {1}\n"
                         "You can overwrite them at your ease.\n").format(
                             defaults['year'], defaults['fullname']))

                if license == 'isc':
                    self.assertEqual(
                        output,
                        ("The template has following defaults:\n"
                         "\tyear: {0}\n"
                         "\tfullname: {1}\n"
                         "\temail: {2}\n"
                         "You can overwrite them at your ease.\n").format(
                             defaults['year'], defaults['fullname'],
                             defaults['email']))

                if license == 'bsd-3-clause':
                    self.assertEqual(
                        output,
                        ("The template has following defaults:\n"
                         "\tyear: {0}\n"
                         "\tfullname: {1}\n"
                         "\tproject: {2}\n"
                         "You can overwrite them at your ease.\n").format(
                             defaults['year'], defaults['fullname'],
                             defaults['project']))
