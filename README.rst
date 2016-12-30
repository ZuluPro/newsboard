Newsboard
=========

Reusable Django app inspired from `Sam et Max's multiboard`_.
It aims to gather serveral type of feed in one app: RSS, Facebook, Sitemap or else.

It uses `Web-Rich-Object` and its `Django integration`_ to handle things.

Install
-------

``pip install newsboard``


Configuration
-------------

Add ``newsboard`` and ``dj_web_rich_object`` in your ``INSTALLED_APPS``.

Create tables: ``./manage.py migrate``

Include this in your URL patterns: ``(r'news/', include('newsboard.urls'))``

Auto-updating
~~~~~~~~~~~~~

To enable auto-updating, please configure your project with celery and use the
configuration in ``newsboard.periodic_tasks.UPDATE_STREAMS``:

::

    sender.add_periodic_task(newsboard.periodic_tasks.UPDATE_STREAMS)


.. _`Sam et Max's multiboard`: https://github.com/sametmax/multiboards
.. _`Web-Rich-Object`: https://github.com/ZuluPro/web-rich-object
.. _`Django integration`: https://github.com/ZuluPro/django-web-rich-object
