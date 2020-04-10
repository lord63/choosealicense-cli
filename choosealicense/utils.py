#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from datetime import date
import os
import subprocess
import time

import click
import requests


doc = 'https://github.com/lord63/choosealicense-cli/wiki/Use-a-github-token-to-get-a-higher-api-rate-limit'


def get_api_response(url):
    headers = {'accept': 'application/vnd.github.drax-preview+json'}
    github_token = os.environ.get('CHOOSEALICENSE_GITHUB_TOKEN', '')
    if github_token != '':
        headers.update({'Authorization': 'token {0}'.format(github_token)})
    try:
        r = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as err:
        raise click.ClickException('send api request failed, error: {0}'.format(err))
    if r.status_code == 403 and r.headers.get('X-RateLimit-Remaining', '') == '0':
        wait_seconds = int(r.headers['X-RateLimit-Reset']) - int(time.time())
        if (wait_seconds) < 60:
            reset_at = '{0} seconds later'.format(wait_seconds)
        else:
            reset_at = '{0} minutes later'.format(wait_seconds / 60)
        raise click.ClickException(
                'Github api rate limit exceeded, limit will be reset {0}. \n'
                'Or you can use a github token to get a higher limit, see doc:\n'
                '{1}'.format(reset_at, doc)
        )
    return r


def _get_git_info(name):
    """Get git configuration info, e.g. user.email."""
    try:
        command_list = ('git config --get user.{0}'.format(name)).split()
        result = subprocess.check_output(command_list).strip().decode('utf-8')
    except subprocess.CalledProcessError:
        raise click.ClickException(
            "Please configure your git(user.{0}).".format(name))
    else:
        return result


def get_default_context():
    """Get the default context for the license template."""
    year = str(date.today().year)
    fullname = _get_git_info('name')
    email = _get_git_info('email')
    return {'year': year, 'fullname': fullname, 'email': email,
            'project': 'the copyright holder'}
