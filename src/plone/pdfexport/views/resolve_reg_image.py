# -*- coding: utf-8 -*-

from AccessControl.ZopeGuards import guarded_getattr
from plone.formwidget.namedfile.converter import b64decode_file
from plone.namedfile.browser import DisplayFile
from plone.namedfile.file import NamedImage
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter, getUtility
from zope.publisher.interfaces import NotFound

from plone.pdfexport import _
from plone.pdfexport.controlpanels.pdf_export import IPdfExportControlPanel


class ResolveRegImage(DisplayFile):

    def __init__(self, context, request):
        super(ResolveRegImage, self).__init__(context, request)
        self.filename = None
        self.data = None
        registry = getUtility(IRegistry)
        settings = registry.forInterface(
            IPdfExportControlPanel,
            prefix="pdfexport",
        )
        if getattr(settings, 'banner', False):
            filename, data = b64decode_file(settings.banner)
            data = NamedImage(data=data, filename=filename)
            self.data = data
            self.filename = filename

    def _getFile(self):
        return self.data
