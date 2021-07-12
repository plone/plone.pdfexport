# -*- coding: utf-8 -*-

from plone.dexterity.browser.view import DefaultView

from plone.pdfexport import _

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class PdfExport(DefaultView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('aspdf.pt')

    def __call__(self):
        # Implement your own actions:
        return super(PdfExport, self).__call__()
