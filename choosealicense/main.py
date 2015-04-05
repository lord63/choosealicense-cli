#!/usr/bin/env python
# -*- coding: utf-8 -*-

import textwrap

import requests
import click
from click.termui import get_terminal_size

from choosealicense import __version__


def print_description(text):
    width, _ = get_terminal_size()
    width = width if width < 78 else 78
    for line in textwrap.wrap(text, width):
        click.echo(line)
    click.echo()


def print_name(name):
    click.secho(name, bold=True)
    click.secho('='*len(name), bold=True)
    click.echo()


def print_rule_list(required, permitted, forbidden):
    max_rule_num = max(list(map(len, [required, permitted, forbidden])))
    for item in [required, permitted, forbidden]:
        if len(item) < max_rule_num:
            item.extend(' '*(max_rule_num-len(item)))
    click.secho('{:<25}'.format('Required'), nl=False, bold=True, fg='blue')
    click.secho('{:<25}'.format('Permitted'), nl=False, bold=True, fg='green')
    click.secho('Forbidden', bold=True, fg='red')
    for i, j, k in zip(required, permitted, forbidden):
        click.secho('{:<25}'.format(i), nl=False)
        click.secho('{:<25}'.format(j), nl=False)
        click.secho(k)


@click.group(context_settings={'help_option_names': ('-h', '--help')})
@click.version_option(__version__, '-v', '--version')
def cli():
    pass


@cli.command()
@click.argument('license')
def info(license):
    response = requests.get(
        'https://api.github.com/licenses/{0}'.format(license),
        headers={'accept': 'application/vnd.github.drax-preview+json'})
    print_name(response.json()['name'])
    print_description(response.json()['description'])
    print_rule_list(response.json()['required'],
                    response.json()['permitted'],
                    response.json()['forbidden'])


@cli.command()
def generate():
    pass


@cli.command()
def content():
    pass
