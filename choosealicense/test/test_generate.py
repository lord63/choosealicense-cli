#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Tests for the `license generate` function
"""

import pytest

from choosealicense.cli import generate, LICENSE_WITH_CONTEXT
from choosealicense.utils import get_default_context


@pytest.mark.usefixtures('mock_api')
class TestGenerate():
    def test_generate_license(self, runner):
        all_the_licenses = (
            'agpl-3.0, apache-2.0, artistic-2.0, bsd-2-clause, '
            'bsd-3-clause, cc0-1.0, epl-1.0, gpl-2.0, gpl-3.0, '
            'isc, lgpl-2.1, lgpl-3.0, mit, mpl-2.0, unlicense')
        for license in all_the_licenses.split(', '):
            result = runner.invoke(generate, [license])
            output, exit_code = result.output, result.exit_code
            assert exit_code == 0

            if license not in LICENSE_WITH_CONTEXT:
                pass

            else:
                defaults = get_default_context()

                if license in ['mit', 'artistic-2.0', 'bsd-2-clause']:
                    assert defaults['fullname'] in output
                    assert defaults['year'] in output

                if license == 'isc':
                    assert defaults['fullname'] in output
                    assert defaults['year'] in output
                    assert defaults['email'] in output

                if license == 'bsd-3-clause':
                    assert defaults['fullname'] in output
                    assert defaults['year'] in output
                    assert defaults['project'] in output

    def test_generate_invalid_license(self, runner):
        result = runner.invoke(generate, ['invalid'])
        output, exit_code = result.output, result.exit_code
        assert exit_code != 0
        assert output == ("Error: Invalid license name, use `license show` "
                          "to get the all available licenses.\n")

    def test_generate_license_with_argument(self, runner):
        result = runner.invoke(generate, ['mit', '--year', '2000'])
        output, exit_code = result.output, result.exit_code
        assert exit_code == 0
        assert '2000' in output
