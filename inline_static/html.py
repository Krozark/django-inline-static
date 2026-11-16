from django.core.exceptions import ImproperlyConfigured


DEFAULT_OPTIONS = {
    # the rules that cannot be inlined (@media, :hover...) stay in a <style> tag
    'keep_at_rules': True,
    # `var(--x)` is replaced by its value: mail clients do not know custom properties
    'resolve_css_variables': True,
    # `width="600"` next to `style="width: 600px"`, for Outlook
    'apply_width_attributes': True,
}


def inline_css(html, css=None, **options):
    """
    Copy the css of an html document into the ``style`` attribute of its tags.

    Mail clients (Gmail, Outlook...) ignore or strip most ``<style>`` tags, so an html email
    needs its styles on the tags themselves. The ``<style>`` tags of ``html`` and the extra
    ``css`` are inlined. ``options`` are given to ``css_inline.inline`` (they replace the
    ``DEFAULT_OPTIONS``).

    Needs the ``email`` extra: ``pip install django-inline-static[email]``.
    """
    try:
        import css_inline
    except ImportError as exc:
        raise ImproperlyConfigured(
            'Inlining html needs css-inline: pip install "django-inline-static[email]"'
        ) from exc

    return css_inline.inline(html, extra_css=css or None, **{**DEFAULT_OPTIONS, **options})
