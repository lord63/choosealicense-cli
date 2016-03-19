#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from datetime import date
from functools import partial
import subprocess

import click
import requests


send_request = partial(
    requests.get,
    headers={'accept': 'application/vnd.github.drax-preview+json'})


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
