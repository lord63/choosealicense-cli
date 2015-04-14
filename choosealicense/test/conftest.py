#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import os

import pytest
import responses
from click.testing import CliRunner

ROOT = path.join(path.abspath(path.dirname(__file__)), 'responses')


@pytest.yield_fixture
def mock_api():
    with open(path.join(ROOT, 'licenses.json')) as f:
        mock_response_body = f.read()
    responses.add(responses.GET, 'https://api.github.com/licenses',
                  body=mock_response_body)

    for license in os.listdir(path.join(ROOT, 'licenses')):
        with open(path.join(ROOT, 'licenses/{0}'.format(license))) as f:
            mock_response_body = f.read()
        responses.add(responses.GET,
                      'https://api.github.com/licenses/{0}'.format(
                          path.splitext(license)[0]),
                      body=mock_response_body, content_type='application/json')
    responses.start()
    yield responses
    responses.stop()


@pytest.fixture(scope='function')
def runner(mock_api):
    return CliRunner()
