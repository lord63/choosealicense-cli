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
        self._print_rule_list(self.info['permissions'],
                              self.info['conditions'],
                              self.info['limitations'])

    def _print_name(self, name):
        """Print the license name in a nice way."""
        secho(name, bold=True)
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

    def _print_rule_list(self, permissions, conditions, limitations):
        """Print the rule list like the way on the web."""
        max_rule_num = max(list(
            map(len, [permissions, conditions, limitations])
        ))
        for item in [permissions, conditions, limitations]:
            if len(item) < max_rule_num:
                item.extend(' '*(max_rule_num-len(item)))
        secho('{:<25}'.format('Permissions'), nl=False, bold=True, fg='green')
        secho('{:<25}'.format('Conditions'), nl=False, bold=True, fg='blue')
        secho('Limitations', bold=True, fg='red')
        for permision, condition, limitation in zip(
                permissions, conditions, limitations):
            secho('{:<25}'.format(permision), nl=False)
            secho('{:<25}'.format(condition), nl=False)
            secho(limitation)
