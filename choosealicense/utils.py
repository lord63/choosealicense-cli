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


def get_default_context():
    """Get the default context for the license template."""
    year = str(date.today().year)
    try:
        fullname = subprocess.check_output(
            'git config --get user.name'.split()
        ).strip().decode('utf-8')
    except subprocess.CalledProcessError:
        raise click.ClickException("Please configure your git(user.name).")
    try:
        email = subprocess.check_output(
            'git config --get user.email'.split()
        ).strip().decode('utf-8')
    except subprocess.CalledProcessError:
        raise click.ClickException("Please configure your git(user.email).")
    return {'year': year, 'fullname': fullname, 'email': email,
            'project': 'the copyright holder'}
