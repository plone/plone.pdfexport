# -*- coding: utf-8 -*-

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import re
from datetime import datetime
from types import BuiltinMethodType

import weasyprint
from bs4 import BeautifulSoup
from plone.app.layout.globals.interfaces import IViewView
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter, getUtility
from zope.interface import alsoProvides

from plone.pdfexport import _
from plone.pdfexport.controlpanels.pdf_export import IPdfExportControlPanel

image_base_url = re.compile("(.*@@images).*")


def plone_url_fetcher(url):
    registry = getUtility(IRegistry)
    pdf_export_settings = registry.forInterface(
        IPdfExportControlPanel, prefix="pdfexport"
    )
    print_image_scale = pdf_export_settings.print_image_scale or "large"
    url_match = image_base_url.match(url)
    groups = url_match.groups()
    if groups:
        url = "{0}/image/{1}".format(groups[0], print_image_scale)
    return weasyprint.default_url_fetcher(url)


class PdfExport(BrowserView):
    def __call__(self):
        default_page = getattr(self.context.aq_explicit, "default_page", None)
        ctx = default_page and self.context.get(default_page) or self.context

        # without this the leadimage viewlet will not be rendered!
        self.request.set("URL", ctx.absolute_url())
        self.request.set("ACTUAL_URL", ctx.absolute_url())

        view_name = getattr(ctx.aq_explicit, "layout", ctx.getDefaultLayout())
        self.context_view = getMultiAdapter((ctx, self.request), name=view_name)
        alsoProvides(self.context_view, IViewView)

        # disable batching for PDF export
        self.context_view._b_size = 100000

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
        pdf = weasyprint.HTML(
            string=html_str, base_url=base_url, url_fetcher=plone_url_fetcher
        ).write_pdf(presentational_hints=True, optimize_images=True)
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
        content_classes = content.get("class", "")
        if content_classes:
            body_classes += " " + content_classes
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
