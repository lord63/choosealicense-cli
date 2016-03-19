#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import re

import click
from click import echo

from choosealicense import __version__
from choosealicense.utils import get_default_context, send_request
from choosealicense.ui import InfoUI


LICENSE_WITH_CONTEXT = ['mit', 'artistic-2.0', 'bsd-2-clause',
                        'bsd-3-clause', 'isc']


@click.group(context_settings={'help_option_names': ('-h', '--help')})
@click.version_option(__version__, '-V', '--version', message='%(version)s')
def cli():
    """ChooseALicense in your terminal."""
    pass  # pragma: no cover


@cli.command()
def show():
    """List all the license."""
    response = send_request('https://api.github.com/licenses')
    keys = [item['key'] for item in response.json()]
    echo(', '.join(keys))


@cli.command()
@click.argument('license')
def info(license):
    """Show the info of the specified license."""
    response = send_request(
        'https://api.github.com/licenses/{0}'.format(license))
    try:
        InfoUI(response.json()).build_ui()
    except KeyError:
        raise click.ClickException("Invalid license name, use `license show` "
                                   "to get the all available licenses.")


@cli.command()
@click.option('--fullname', '-f', help="Copyright holder's name")
@click.option('--year', '-y', help="Copyright year")
@click.option('--email', '-e', help="Copyright holder's email")
@click.option('--project', '-p', help="The project organization")
@click.argument('license')
def generate(license, fullname, year, email, project):
    """Generate the specified license."""
    response = send_request(
        'https://api.github.com/licenses/{0}'.format(license))

    try:
        license_template = response.json()['body']
    except KeyError:
        raise click.ClickException("Invalid license name, use `license show` "
                                   "to get the all available licenses.")

    if license not in LICENSE_WITH_CONTEXT:
        echo(license_template, nl=False)
    else:
        context_variable = re.findall(r'\[(\w+)\]', response.json()['body'])
        raw_context = {'fullname': fullname, 'year': year, 'email': email,
                       'project': project}
        user_context = {key: value for (key, value) in raw_context.items()
                        if value is not None}
        context = get_default_context()
        context.update(user_context)
        for item in context_variable:
            license_template = license_template.replace('[{0}]'.format(item),
                                                        context[item])
        echo(license_template, nl=False)


@cli.command()
@click.argument('license')
def context(license):
    """Show the default context for the license."""
    if license not in LICENSE_WITH_CONTEXT:
        echo("Just use it, there's no context for the license.")
    else:
        response = send_request(
            'https://api.github.com/licenses/{0}'.format(license))
        context = re.findall(r'\[(\w+)\]', response.json()['body'])
        default_context = get_default_context()
        echo('The template has following defaults:')
        for item in context:
            echo('\t{0}: {1}'.format(item, default_context[item]))
        echo('You can overwrite them at your ease.')
