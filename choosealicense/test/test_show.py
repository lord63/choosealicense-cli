#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Tests for the `license show` function
"""

import pytest

from choosealicense.cli import show


@pytest.mark.usefixtures('mock_api')
class TestShow():
    def test_show_all_the_licenses(self, runner):
        result = runner.invoke(show)
        it_should_be = ('agpl-3.0, apache-2.0, bsd-2-clause, '
                        'bsd-3-clause, epl-2.0, gpl-2.0, gpl-3.0, '
                        'lgpl-2.1, lgpl-3.0, mit, mpl-2.0, unlicense')
        assert result.exit_code == 0
        assert result.output.strip() == it_should_be
