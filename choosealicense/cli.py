#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import click
from click import echo
import requests

from choosealicense import __version__
from choosealicense.utils import (print_name, print_description,
                                  print_rule_list, get_default_context)


LICENSE_WITH_CONTEXT = ['mit', 'artistic-2.0', 'bsd-2-clause',
                        'bsd-3-clause', 'isc']


@click.group(context_settings={'help_option_names': ('-h', '--help')})
@click.version_option(__version__, '-v', '--version', message='%(version)s')
def cli():
    """ChooseALicense in your terminal."""
    pass


@cli.command()
def show():
    """List all the license."""
    response = requests.get(
        'https://api.github.com/licenses',
        headers={'accept': 'application/vnd.github.drax-preview+json'})
    keys = [item['key'] for item in response.json()]
    echo(', '.join(keys))


@cli.command()
@click.argument('license')
def info(license):
    """Show the info of the specified license."""
    response = requests.get(
        'https://api.github.com/licenses/{0}'.format(license),
        headers={'accept': 'application/vnd.github.drax-preview+json'})
    try:
        print_name(response.json()['name'])
        print_description(response.json()['description'])
        print_rule_list(response.json()['required'],
                        response.json()['permitted'],
                        response.json()['forbidden'])
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
    response = requests.get(
        'https://api.github.com/licenses/{0}'.format(license),
        headers={'accept': 'application/vnd.github.drax-preview+json'})

    try:
        license_template = response.json()['body']
    except KeyError:
        raise click.ClickException("Invalid license name, use `license show` "
                                   "to get the all available licenses.")

    if license not in LICENSE_WITH_CONTEXT:
        echo(license_template, nl=False)
    else:
        context = re.findall(r'\[(\w+)\]', response.json()['body'])
        raw_context = {'fullname': fullname, 'year': year, 'email': email,
                       'project': project}
        user_context = {key: value for (key, value) in raw_context.items()
                        if value is not None}
        default_context = get_default_context()
        for (key, value) in user_context.items():
            default_context[key] = value
        for item in context:
            license_template = license_template.replace('[{0}]'.format(item),
                                                        default_context[item])
        echo(license_template, nl=False)


@cli.command()
@click.argument('license')
def context(license):
    """Show the default context for the license."""
    if license not in LICENSE_WITH_CONTEXT:
        echo("Just use it, there's no context for the license.")
    else:
        response = requests.get(
            'https://api.github.com/licenses/{0}'.format(license),
            headers={'accept': 'application/vnd.github.drax-preview+json'})
        context = re.findall(r'\[(\w+)\]', response.json()['body'])
        default_context = get_default_context()
        echo('The template has following defaults:')
        for item in context:
            echo('\t{0}: {1}'.format(item, default_context[item]))
        echo('You can overwrite them at your ease.')
