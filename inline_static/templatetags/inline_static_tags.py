from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from inline_static.css import transform_css_urls
from inline_static.html import inline_css
from inline_static.loader import load_staticfile


register = template.Library()


@register.simple_tag
def inline_staticfile(name):
    return load_staticfile(name, fail_silently=not settings.DEBUG)


@register.simple_tag
def inline_style(name):
    return mark_safe(
        load_staticfile(name, transform_css_urls, fail_silently=not settings.DEBUG)
    )


@register.simple_tag
def inline_javascript(name):
    return mark_safe(load_staticfile(name, fail_silently=not settings.DEBUG))


class InlineHtmlNode(template.Node):
    def __init__(self, nodelist, names):
        self.nodelist = nodelist
        self.names = names

    def render(self, context):
        css = '\n'.join(
            load_staticfile(
                name.resolve(context), transform_css_urls, fail_silently=not settings.DEBUG
            )
            for name in self.names
        )
        return mark_safe(inline_css(self.nodelist.render(context), css))


@register.tag
def inline_html(parser, token):
    """
    Render the block, then copy its css into the ``style`` attribute of its tags (for emails).

    The ``<style>`` tags of the block are inlined, and so are the static css files given as
    arguments. Needs the ``email`` extra (css-inline).

    .. code-block:: text

        {% inline_html 'css/email.css' %}
            <html>...</html>
        {% end_inline_html %}
    """
    names = [parser.compile_filter(bit) for bit in token.split_contents()[1:]]
    nodelist = parser.parse(('end_inline_html',))
    parser.delete_first_token()
    return InlineHtmlNode(nodelist, names)
