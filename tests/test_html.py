from unittest import mock

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.template import Context, Template

from inline_static.html import inline_css
from inline_static.loader import load_staticfile


HTML = '<html><head></head><body><p class="lead">Hello</p></body></html>'


class TestInlineCss:
    def test_the_css_goes_into_the_style_attribute(self):
        result = inline_css(HTML, '.lead { color: red; }')

        assert 'style="color: red;"' in result
        assert '<style' not in result

    def test_the_style_tags_of_the_document_are_inlined(self):
        html = '<html><head><style>.lead { color: red; }</style></head><body><p class="lead">x</p></body></html>'

        assert 'style="color: red;"' in inline_css(html)

    def test_variables_are_resolved(self):
        result = inline_css(HTML, ':root { --accent: #00daff; } .lead { color: var(--accent); }')

        assert 'color: #00daff' in result
        assert 'var(' not in result

    def test_at_rules_stay_in_a_style_tag(self):
        result = inline_css(HTML, '@media (max-width: 480px) { .lead { font-size: 14px; } }')

        assert '@media' in result

    def test_options_replace_the_defaults(self):
        result = inline_css(HTML, '@media (max-width: 480px) { .lead { font-size: 14px; } }', keep_at_rules=False)

        assert '@media' not in result

    def test_without_css_inline_the_error_says_what_to_install(self):
        with mock.patch.dict('sys.modules', {'css_inline': None}):
            with pytest.raises(ImproperlyConfigured) as exc:
                inline_css(HTML)

        assert 'django-inline-static[email]' in str(exc.value)


class TestInlineHtmlTag:
    def setup(self):
        load_staticfile._cache.clear()

    def render(self, source):
        return Template('{% load inline_static_tags %}' + source).render(Context())

    def test_the_static_files_are_inlined_in_the_block(self, settings):
        settings.DEBUG = True  # the files are found by the finders, without collectstatic
        result = self.render(
            "{% inline_html 'css/email.css' %}" + HTML + '{% end_inline_html %}'
        )

        assert 'color: #00daff' in result
        assert 'font-size: 18px' in result
        assert '@media' in result

    def test_the_block_without_files(self):
        result = self.render(
            '{% inline_html %}<html><head><style>.lead { color: red; }</style></head>'
            '<body><p class="lead">x</p></body></html>{% end_inline_html %}'
        )

        assert 'style="color: red;"' in result
