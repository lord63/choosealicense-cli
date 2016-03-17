#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import re
import textwrap

from click import echo, secho
from click.termui import get_terminal_size


def print_name(name):
    """Print the license name in a nice way."""
    secho(name, bold=True)
    secho('='*len(name), bold=True)
    echo()


def print_description(text):
    """Print the short description for the license."""
    # Strip the link tag, but this solution is not elegant enough.
    for link in re.findall(r'<a href=[^<]*</a>', text):
        text = text.replace(link,
                            re.search(r'(?<=">).*(?=</a>)', link).group())
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
