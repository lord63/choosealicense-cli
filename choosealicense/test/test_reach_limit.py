#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Tests when you reach github api limit
"""

from os import path
import time

import responses
from click.testing import CliRunner

from choosealicense.cli import show


ROOT = path.join(path.abspath(path.dirname(__file__)), 'responses')
with open(path.join(ROOT, 'reach_limit.json')) as f:
    mock_response_body = f.read()


def test_reach_limit_and_reset_30_minutes_later():
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.Response(
                method='GET',
                url='https://api.github.com/licenses',
                body=mock_response_body,
                content_type='application/json',
                headers={'X-RateLimit-Remaining': '0', 'X-RateLimit-Reset': str(int(time.time())+35*60)},
                status=403,
            )
        )
        result = CliRunner().invoke(show)
        assert 'api rate limit exceeded' in result.output
        assert 'minutes later' in result.output


def test_reach_limit_and_reset_30_seconds_later():
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.Response(
                method='GET',
                url='https://api.github.com/licenses',
                body=mock_response_body,
                content_type='application/json',
                headers={'X-RateLimit-Remaining': '0', 'X-RateLimit-Reset': str(int(time.time())+15)},
                status=403,
            )
        )
        result = CliRunner().invoke(show)
        assert 'api rate limit exceeded' in result.output
        assert 'seconds later' in result.output
