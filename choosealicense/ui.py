#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import re
import textwrap

from click import echo, secho
from click.termui import get_terminal_size


class InfoUI(object):
    def __init__(self, info):
        self.info = info

    def build_ui(self):
        """Build the CLI UI for `license info`."""
        self._print_name(self.info['name'])
        self._print_description(self.info['description'])
        self._print_rule_list(self.info['required'],
                              self.info['permitted'],
                              self.info['forbidden'])

    def _print_name(self, name):
        """Print the license name in a nice way."""
        secho(name, bold=True)
        secho('='*len(name), bold=True)
        echo()

    def _print_description(self, text):
        """Print the short description for the license."""
        # Strip the link tag, but this solution is not elegant enough.
        tag_with_text_re = r'<a href=[^<]*</a>'
        text_in_tag_re = r'(?<=">).*(?=</a>)'
        for link in re.findall(tag_with_text_re, text):
            text = text.replace(link, re.search(text_in_tag_re, link).group())
        width, _ = get_terminal_size()
        width = width if width < 78 else 78
        for line in textwrap.wrap(text, width):
            echo(line)
        echo()

    def _print_rule_list(self, required, permitted, forbidden):
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
