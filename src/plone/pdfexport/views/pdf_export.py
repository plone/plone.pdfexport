# -*- coding: utf-8 -*-

from datetime import datetime

import weasyprint
from bs4 import BeautifulSoup
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter, getUtility

from plone.pdfexport import _
from plone.pdfexport.controlpanels.pdf_export import IPdfExportControlPanel

# from plone.dexterity.browser.view import DefaultView
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class PdfExport(BrowserView):
    def __call__(self):
        default_page = getattr(self.context.aq_explicit, "default_page", None)
        ctx = default_page and self.context.get(default_page) or self.context
        view_name = getattr(ctx.aq_explicit, "layout", ctx.getDefaultLayout())
        self.context_view = getMultiAdapter((ctx, ctx.REQUEST), name=view_name)
        # disable batching for PDF export
        self.context_view._b_size = 10000
        if self.request.form.get("html"):
            return self.render_html()
        return self.render_pdf()

    @property
    def get_styles(self):
        registry = getUtility(IRegistry)
        pdf_export_settings = registry.forInterface(
            IPdfExportControlPanel, prefix="pdfexport"
        )
        return pdf_export_settings.print_css

    def render_html(self):
        html_str = self.context_view.index()
        html_str = self._clean_html(html_str)
        return html_str

    def render_pdf(self):
        cstate = getMultiAdapter(
            (self.context, self.request), name="plone_context_state"
        )
        base_url = cstate.current_base_url()
        html_str = self.context_view.index()
        filename = self._filename()
        html_str = self._clean_html(html_str)
        pdf = weasyprint.HTML(string=html_str, base_url=base_url).write_pdf()
        self.request.response.setHeader("Content-Type", "application/pdf")
        self.request.response.setHeader(
            "Content-Disposition", "inline;filename=%s" % filename
        )
        self.request.response.setHeader("Content-Length", len(pdf))
        return pdf

    def _clean_html(self, raw_html):
        content_soup = BeautifulSoup(raw_html, "html.parser")
        body_classes = content_soup.select_one("body")["class"]
        content = content_soup.select_one("#content")
        # copy body css classes to content tag, for later usage in print css
        content["class"] = body_classes
        html_frame = self.index()
        frame_soup = BeautifulSoup(html_frame, "html.parser")
        frame_soup.select_one("#pdf-content").replace_with(content)
        return str(frame_soup)

    def _filename(self):
        filename = self.context.id
        now = datetime.now()
        filename += "{0}{1}{2}_{3}{4}.pdf".format(
            now.year, now.month, now.day, now.hour, now.minute
        )
        return filename
