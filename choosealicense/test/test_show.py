#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Tests for the `license show` function
"""

import unittest

from click.testing import CliRunner

from choosealicense.main import show


class TestShow(unittest.TestCase):
    def test_show_all_the_licenses(self):
        runner = CliRunner()
        result = runner.invoke(show)
        it_should_be = ('agpl-3.0, apache-2.0, artistic-2.0, bsd-2-clause, '
                        'bsd-3-clause, cc0-1.0, epl-1.0, gpl-2.0, gpl-3.0, '
                        'isc, lgpl-2.1, lgpl-3.0, mit, mpl-2.0, unlicense')
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.strip(), it_should_be)
