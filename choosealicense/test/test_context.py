#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Tests for the `license context` function
"""

import pytest

from choosealicense.cli import context, LICENSE_WITH_CONTEXT
from choosealicense.utils import get_default_context


context_template = u'''\
The template has following defaults:
\tyear: {0}
\tfullname: {1}
You can overwrite them at your ease.
'''
context_with_email_template = u'''\
The template has following defaults:
\tyear: {0}
\tfullname: {1}
\temail: {2}
You can overwrite them at your ease.
'''


@pytest.mark.usefixtures('mock_api')
class TestContext():
    def test_show_license_context(self, runner):
        all_the_licenses = (
            'agpl-3.0, apache-2.0, bsd-2-clause, '
            'bsd-3-clause, epl-2.0, gpl-2.0, gpl-3.0, '
            'lgpl-2.1, lgpl-3.0, mit, mpl-2.0, unlicense')
        for license in all_the_licenses.split(', '):
            result = runner.invoke(context, [license])
            output, exit_code = result.output, result.exit_code
            assert exit_code == 0
            if license not in LICENSE_WITH_CONTEXT:
                assert output == ("Just use it, there's no context "
                                  "for the license.\n")
            else:
                defaults = get_default_context()

                if license in ['mit', 'artistic-2.0', 'bsd-2-clause', 'bsd-3-clause']:
                    assert output == context_template.format(
                        defaults['year'], defaults['fullname'])

                if license == 'isc':
                    assert output == context_with_email_template.format(
                            defaults['year'], defaults['fullname'],
                            defaults['email'])
