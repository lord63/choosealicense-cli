#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from datetime import date
import subprocess
import textwrap

import click
from click import echo, secho
from click.termui import get_terminal_size


def print_name(name):
    """Print the license name in a nice way."""
    secho(name, bold=True)
    secho('='*len(name), bold=True)
    echo()


def print_description(text):
    """Print the short description for the license."""
    width, _ = get_terminal_size()
    width = width if width < 78 else 78
    for line in textwrap.wrap(text, width):
        echo(line)
    echo()


def print_rule_list(required, permitted, forbidden):
    """Print the rule list like the way on the web."""
    max_rule_num = max(list(map(len, [required, permitted, forbidden])))
    for item in [required, permitted, forbidden]:
        if len(item) < max_rule_num:
            item.extend(' '*(max_rule_num-len(item)))
    secho('{:<25}'.format('Required'), nl=False, bold=True, fg='blue')
    secho('{:<25}'.format('Permitted'), nl=False, bold=True, fg='green')
    secho('Forbidden', bold=True, fg='red')
    for require, permit, forbid in zip(required, permitted, forbidden):
        secho('{:<25}'.format(require), nl=False)
        secho('{:<25}'.format(permit), nl=False)
        secho(forbid)


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
