Usage
=====

Loading static files
--------------------

To inline any static file in your template, use the ``inline_static_tags`` tag.
The inlined content is not marked safe, do this by yourself if you're sure that
the included content is safe for html documents.

.. code-block:: text

    {% load inline_static_tags %}

    {% inline_staticfile 'build/fake.txt' %}

    <!-- or -->

    {% inline_staticfile 'build/image.svg' as image %}{{ image|safe }}


Inlining javascript
-------------------

If you want to inline javascript code, use the ``inline_javascript`` tag.
The inlined content will be marked as safe.

.. code-block:: text

    {% load inline_static_tags %}

    <script>{% inline_javascript 'build/critical.pkg.js' %}</script>


Inlining styles
---------------

To inline a css styles file, use the ``inline_style`` template tag.

The styles will be transformed by replacing any relative url in the content with
absolute urls to make sure fonts, background images and other ``url()`` calls
work after including.

.. code-block:: text

    {% load inline_static_tags %}

    <style type="text/css">{% inline_style 'build/all.css' %}</style>


Inlining styles in the tags (emails)
------------------------------------

Mail clients (Gmail, Outlook...) ignore or strip most ``<style>`` tags: the styles must be on
the tags themselves. The ``inline_html`` block tag renders its content, then copies the css
into the ``style`` attribute of each tag. It needs the ``email`` extra:
``pip install "django-inline-static[email]"``.

The ``<style>`` tags of the block and the static css files given as arguments are inlined.
``var(--x)`` is replaced by its value, and the rules that cannot be inlined (``@media``,
``:hover``) stay in a ``<style>`` tag.

.. code-block:: text

    {% load inline_static_tags %}

    {% inline_html 'css/email.css' %}
        <html>
            <body><p class="lead">Hello</p></body>
        </html>
    {% end_inline_html %}

Write the css of an email without nesting: css-inline does not flatten nested rules. The
function ``inline_static.html.inline_css(html, css=None, **options)`` does the same outside of a
template.

