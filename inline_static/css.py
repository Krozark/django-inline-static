# Based on some ideas from
# https://github.com/django-compressor/django-compressor/
#   blob/develop/compressor/filters/css_default.py

import posixpath
import re

from django.conf import settings


class CssUrlTransformer(object):
    SCHEMES = ('http://', 'https://', '/')
    URL_PATTERN = re.compile(
        r"""
        url\(
        \s*      # any amount of whitespace
        ([\'"]?) # optional quote
        (.*?)    # any amount of anything, non-greedily (this is the actual url)
        \1       # matching quote (or nothing if there was none)
        \s*      # any amount of whitespace
        \)""",
        re.VERBOSE,
    )
    IMPORT_PATTERN = re.compile(
        r"""
        @import
        \s*      # any amount of whitespace
        ([\'"])  # quote
        (.*?)    # any amount of anything, non-greedily (this is the actual url)
        \1       # matching quote (or nothing if there was none)
        \s*      # any amount of whitespace
        ;""",
        re.VERBOSE,
    )

    def __init__(self, name, path, content, base_url=None):
        self.name = name
        self.path = path
        self.content = content

        self.base_scheme_domain, self.base_url = self.parse_static_url(
            base_url or settings.STATIC_URL
        )
        self.url = '{0}/{1}'.format(self.base_url, posixpath.dirname(self.name))

    def parse_static_url(self, base_url):
        if base_url.startswith(('http://', 'https://', '//')):
            base_url_parts = base_url.split('/')

            scheme_domain = '/'.join(base_url_parts[:3])
            base_url = '/'.join(base_url_parts[3:])
        else:
            scheme_domain = None

        return scheme_domain, base_url.rstrip('/')

    def transform(self):
        transformed = self.content
        transformed = self.IMPORT_PATTERN.sub(self.transform_import, transformed)
        transformed = self.URL_PATTERN.sub(self.transform_url, transformed)
        return transformed

    def transform_url(self, match):
        return 'url({quote}{url}{quote})'.format(
            quote=match.group(1), url=self.resolve_url(match.group(2))
        )

    def resolve_url(self, url):
        # Skip base64, etc. and external or already absolute paths
        if url.startswith(('#', 'data:')) or url.startswith(self.SCHEMES):
            return url

        resolved_url = posixpath.normpath('/'.join([self.url, url]))
        if self.base_scheme_domain:
            resolved_url = '{0}/{1}'.format(self.base_scheme_domain, resolved_url.lstrip('/'))
        return resolved_url

    def transform_import(self, match):
        # recurse on @import to include them
        from inline_static.templatetags.inline_static_tags import inline_style

        url = match.group(2)
        resolve_url = self.resolve_url(url)
        if resolve_url.startswith(settings.STATIC_URL):
            resolve_url = resolve_url[len(settings.STATIC_URL) :]
        style = inline_style(resolve_url)
        return style


def transform_css_urls(*args, **kwargs):
    return CssUrlTransformer(*args, **kwargs).transform()
