#!/usr/bin/env python
# -*- coding: utf-8 -*-

import textwrap
import re
from datetime import date
import subprocess

import requests
import click
from click import echo, secho
from click.termui import get_terminal_size

from choosealicense import __version__


LICENSE_WITH_CONTEXT = ['mit', 'artistic-2.0', 'bsd-2-clause',
                        'bsd-3-clause', 'isc']


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
    except Exception:
        echo("WARNING: Please configure your git(user.name).\n")
        raise
    try:
        email = subprocess.check_output(
            'git config --get user.email'.split()
        ).strip().decode('utf-8')
    except Exception:
        echo("WARNING: Please configure your git(user.email).\n")
        raise
    return {'year': year, 'fullname': fullname, 'email': email,
            'project': 'the copyright holder'}


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
    print_name(response.json()['name'])
    print_description(response.json()['description'])
    print_rule_list(response.json()['required'],
                    response.json()['permitted'],
                    response.json()['forbidden'])


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
    license_template = response.json()['body']
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
