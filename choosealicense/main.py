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


LICENSE_WITH_CONTEXT = ['mit', 'artistic-2.0', 'bsd-2-clause', 'bsd-3-clause',
                        'isc', 'unlicense']


def print_description(text):
    width, _ = get_terminal_size()
    width = width if width < 78 else 78
    for line in textwrap.wrap(text, width):
        echo(line)
    echo()


def print_name(name):
    secho(name, bold=True)
    secho('='*len(name), bold=True)
    echo()


def print_rule_list(required, permitted, forbidden):
    max_rule_num = max(list(map(len, [required, permitted, forbidden])))
    for item in [required, permitted, forbidden]:
        if len(item) < max_rule_num:
            item.extend(' '*(max_rule_num-len(item)))
    secho('{:<25}'.format('Required'), nl=False, bold=True, fg='blue')
    secho('{:<25}'.format('Permitted'), nl=False, bold=True, fg='green')
    secho('Forbidden', bold=True, fg='red')
    for i, j, k in zip(required, permitted, forbidden):
        secho('{:<25}'.format(i), nl=False)
        secho('{:<25}'.format(j), nl=False)
        secho(k)


def get_default_context():
    year = str(date.today().year)
    try:
        fullname = subprocess.check_output(
            'git config --get user.name'.split()
        ).strip().decode('utf-8')
    except Exception:
        print("WARNING: Please configure your git. I need your user name.\n")
        raise
    try:
        email = subprocess.check_output(
            'git config --get user.email'.split()
        ).strip().decode('utf-8')
    except Exception:
        print("WARNING: Please configure your git. I need your email.\n")
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
@click.argument('license')
def generate(license):
    """Generate the specified license."""
    response = requests.get(
        'https://api.github.com/licenses/{0}'.format(license),
        headers={'accept': 'application/vnd.github.drax-preview+json'})
    license_template = response.json()['body']
    if license not in LICENSE_WITH_CONTEXT:
        echo(license_template, nl=False)
    else:
        context = re.findall(r'\[(\w+)\]', response.json()['body'])
        default_context = get_default_context()
        for item in context:
            license_template = license_template.replace('[{0}]'.format(item),
                                                default_context[item])
        echo(license_template, nl=False)


@cli.command()
@click.argument('license')
def context(license):
    """Show the default context for the license."""
    if license not in LICENSE_WITH_CONTEXT:
        print "Just use it, there's no context for the license."
    else:
        response = requests.get(
            'https://api.github.com/licenses/{0}'.format(license),
            headers={'accept': 'application/vnd.github.drax-preview+json'})
        context = re.findall(r'\[(\w+)\]', response.json()['body'])
        default_context = get_default_context()
        for item in context:
            echo('{0}: {1}'.format(item, default_context[item]))
