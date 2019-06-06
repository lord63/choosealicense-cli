#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Tests for the `license info` function
"""

import pytest

from choosealicense.cli import info


@pytest.mark.usefixtures('mock_api')
class TestInfo():
    def test_show_license_info(self, runner):
        all_the_licenses = {
            'agpl-3.0': ('GNU Affero General Public License v3.0', 12),
            'apache-2.0': ('Apache License 2.0', 10),
            'bsd-2-clause': ('BSD 2-Clause "Simplified" License', 7),
            'bsd-3-clause': ('BSD 3-Clause "New" or "Revised" License', 7),
            'epl-2.0': ('Eclipse Public License 2.0', 10),
            'gpl-2.0': ('GNU General Public License v2.0', 10),
            'gpl-3.0': ('GNU General Public License v3.0', 11),
            'lgpl-2.1': ('GNU Lesser General Public License v2.1', 10),
            'lgpl-3.0': ('GNU Lesser General Public License v3.0', 11),
            'mit': ('MIT License', 7),
            'mpl-2.0': ('Mozilla Public License 2.0', 11),
            'unlicense': ('The Unlicense', 6)
        }

        for short_name, fullname_and_rules_number in all_the_licenses.items():
            result = runner.invoke(info, [short_name])
            output, exit_code = result.output, result.exit_code
            rules = output.split('Limitations\n')[1].split('\n')
            flat_rules = sum([item.split() for item in rules], [])
            fullname, rules_number = fullname_and_rules_number

            assert exit_code == 0
            assert '</a>' not in output
            assert fullname in output
            assert '{0:<25}{1:<25}{2}'.format(
                'Permissions', 'Conditions', 'Limitations') in output
            assert rules_number == len(flat_rules)

    def test_show_invalid_license_info(self, runner):
        result = runner.invoke(info, ['invalid'])
        output, exit_code = result.output, result.exit_code
        assert exit_code != 0
        assert output == ("Error: Invalid license name, use `license show` "
                          "to get the all available licenses.\n")
