#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Tests for the `license generate` function
"""

from click.testing import CliRunner

from choosealicense.main import (generate, LICENSE_WITH_CONTEXT,
                                 get_default_context)


def test_generate_license():
    all_the_licenses = ('agpl-3.0, apache-2.0, artistic-2.0, bsd-2-clause, '
                        'bsd-3-clause, cc0-1.0, epl-1.0, gpl-2.0, gpl-3.0, '
                        'isc, lgpl-2.1, lgpl-3.0, mit, mpl-2.0, unlicense')
    runner = CliRunner()
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