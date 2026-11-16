Changelog
=========

0.2.0
-----

* Add the ``inline_html`` block tag and ``inline_static.html.inline_css()``: the css of an
  html document is copied into the ``style`` attribute of its tags, for emails (needs the
  ``email`` extra, css-inline). ``var(--x)`` is resolved, ``@media`` rules are kept.

0.1.0 (2019-03-19)
------------------

* Ensure that inline static included the hashed versions of a static file when
  filename hashing is available in the staticfiles storage.


0.0.1 (2018-08-08)
------------------

* Initial release of `django-inline-static`
