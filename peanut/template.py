#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Template"""

import peanut
import jinja2
from os import path
from jinja2 import FileSystemLoader
from jinja2.exceptions import TemplateNotFound


class SmartLoader(FileSystemLoader):
    """A smart template loader"""

    available_extension = ['.html', '.xml']

    def get_source(self, environment, template):
        if template is None:
            raise TemplateNotFound(template)
        if '.' in template:
            return super(SmartLoader, self).get_source(environment, template)

        for extension in SmartLoader.available_extension:
            try:
                filename = template + extension
                return super(SmartLoader, self).get_source(environment, filename)
            except TemplateNotFound:
                pass

        raise TemplateNotFound(template)


class Template(object):
    """Template"""

    def __init__(self, path, **kwargs):
        loader = SmartLoader(path)
        self.env = jinja2.Environment(
            loader=loader,
            autoescape=True
        )
        # Update global namesapce
        self.env.globals.update(kwargs)

    def render(self, name, **context):
        """Render template with name and context"""

        template = self.env.get_template(name)
        template.render(**context)
