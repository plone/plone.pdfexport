.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://github.com/plone/plone.pdfexport/actions/workflows/plone-package.yml/badge.svg
    :target: https://github.com/plone/plone.pdfexport/actions/workflows/plone-package.yml

.. image:: https://coveralls.io/repos/github/plone/plone.pdfexport/badge.svg?branch=main
    :target: https://coveralls.io/github/plone/plone.pdfexport?branch=main
    :alt: Coveralls

.. image:: https://img.shields.io/pypi/v/plone.pdfexport.svg
    :target: https://pypi.python.org/pypi/plone.pdfexport/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/plone.pdfexport.svg
    :target: https://pypi.python.org/pypi/plone.pdfexport
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/plone.pdfexport.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/plone.pdfexport.svg
    :target: https://pypi.python.org/pypi/plone.pdfexport/
    :alt: License


===============
plone.pdfexport
===============

Provides PDF export functionality for Plone content.

Features
--------

- Exports Documents, Event, News items and other custom content.
- Can be customized via CSS in the PDF Export control panel.
- Long tables which will be rendered on more than one page, will have the thead repeated on every page.
- One can use Plone body tag CSS classes to define CSS rules for specific Plone content.

This add-on is based on the great `WeasyPrint library <https://weasyprint.org>`_.

Translations
------------

This product has been translated into

- english
- german


Installation
------------

Install plone.pdfexport by adding it to your buildout::

    [buildout]

    ...

    eggs =
        plone.pdfexport


and then running ``bin/buildout``

Usage
-----

After installing the add-on you can call the "aspdf" view on any Plone content.

``http://localhost:8080/Plone/news/aspdf``

for testing, you can add the GET parameter "html=1" to see the HTML version before it get rendered into a PDF.

``http://localhost:8080/Plone/news/aspdf?html=1``


Authors
-------

This add-on was build by `Derico <https://derico.de>`_ [MrTango].


Contribute
----------

- Issue Tracker: https://github.com/plone/plone.pdfexport/issues
- Source Code: https://github.com/plone/plone.pdfexport


Support
-------

If you are having issues, please let us know.


License
-------

The project is licensed under the GPLv2.
