# -*- coding: utf-8 -*-

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import re
from datetime import datetime

import weasyprint
from bs4 import BeautifulSoup
from plone import api
from plone.app.layout.globals.interfaces import IViewView
from plone.formwidget.namedfile.converter import b64decode_file
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter, getUtility
from zope.interface import alsoProvides
from zope.site.hooks import getSite

from plone.pdfexport.controlpanels.pdf_export import IPdfExportControlPanel

image_base_url = re.compile(r"(.*@@images).*")
pdf_banner_url = re.compile(r"(.*@@pdf-banner)/(.*)/?.*")


def getBannerImage(site=None):
    if site is None:
        site = getSite()
    registry = getUtility(IRegistry)
    settings = registry.forInterface(
        IPdfExportControlPanel,
        prefix="pdfexport",
        check=False,
    )
    site_url = site.absolute_url()
    if getattr(settings, 'banner', False):
        filename, data = b64decode_file(settings.banner)
        return '{}/@@pdf-banner/{}'.format(
            site_url, filename)
    else:
        return '%s/logo.png' % site_url


def plone_url_fetcher(url):
    registry = getUtility(IRegistry)
    pdf_export_settings = registry.forInterface(
        IPdfExportControlPanel, prefix="pdfexport"
    )
    print_image_scale = pdf_export_settings.print_image_scale or "large"
    portal = getSite()
    pstate = getMultiAdapter((portal, portal.REQUEST), name="plone_portal_state")
    purl = pstate.portal_url()
    images_url_match = image_base_url.match(url)
    pdf_url_match = pdf_banner_url.match(url)
    if images_url_match:
        # get the image configured image scale:
        groups = images_url_match.groups()
        base_url = u""
        if groups:
            url = "{0}/image/{1}".format(groups[0], print_image_scale)
            base_url = groups[0]
        scaling_view = portal.unrestrictedTraverse(
            base_url.replace(purl, "").lstrip("/")
        )
        scaled_image = scaling_view.scale("image", scale=print_image_scale)
        image_file = scaled_image.data.open()
    elif pdf_url_match:
        # get pdf-banner, something special, comes from registry
        groups = pdf_url_match.groups()
        if groups:
            pdf_view = api.content.get_view(
                "pdf-banner",
                context=portal,
                request=portal.REQUEST,
            )
            # pdf_banner_view = pdf_view.publishTraverse(portal.REQUEST, groups[1])
            image_file = pdf_view()
            # return directly but as string
            return dict(string=image_file)
    else:
        # get the original image:
        image_obj = portal.unrestrictedTraverse(url.replace(purl, "").lstrip("/"), None)
        if image_obj:
            image_file = image_obj.image.open()
    return dict(file_obj=image_file)


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
            return self.render_preview()
        return self.render_pdf()

    @property
    def canonical_url(self):
        cstate = getMultiAdapter(
            (self.context, self.request), name="plone_context_state"
        )
        return cstate.canonical_object_url()

    @property
    def get_styles(self):
        mode = api.portal.get_registry_record('pdfexport.default_mode')
        mode = self.request.get('mode') or mode
        page_css = api.portal.get_registry_record("pdfexport.{0}_css".format(mode))
        print_css = api.portal.get_registry_record('pdfexport.print_css')
        css = "{0}{1}".format(page_css, print_css)
        return css

    @property
    def img_src(self):
        return getBannerImage()

    def render_preview(self):
        html_str = self.render_html()
        soup = BeautifulSoup(html_str, "html.parser")
        style_tag = soup.new_tag("style")
        style_tag.string = """
body {
    margin: 2.5cm 1.4cm 2.75cm 1.4cm;
    position: relative;
}
header.pdf-header {top: 0;}
"""
        head = soup.find("head")
        head.append(style_tag)
        return str(soup)

    def render_html(self):
        html_str = self.context_view()
        html_str = self._clean_html(html_str)
        return html_str

    def render_pdf(self):
        cstate = getMultiAdapter(
            (self.context, self.request), name="plone_context_state"
        )
        base_url = cstate.current_base_url()
        html_str = self.render_html()
        filename = self._filename()
        pdf = weasyprint.HTML(
            string=html_str, base_url=base_url, url_fetcher=plone_url_fetcher
        ).write_pdf(presentational_hints=True)
        self.request.response.setHeader("Content-Type", "application/pdf")
        self.request.response.setHeader(
            "Content-Disposition", "inline;filename=%s" % filename
        )
        self.request.response.setHeader("Content-Length", len(pdf))
        return pdf

    def _clean_html(self, raw_html):
        content_soup = BeautifulSoup(raw_html, "html.parser")
        content = content_soup.select_one("#content")
        body = content_soup.select_one("body")
        body_classes = body.get("class")

        # copy body css classes to content tag, for later usage in print css
        if body_classes:
            content_classes = content.get("class", [])
            body_classes.extend(content_classes)
            content["class"] = body_classes

        html_frame = self.index()
        frame_soup = BeautifulSoup(html_frame, "html.parser")
        frame_soup.select_one("#pdf-content").replace_with(content)
        return str(frame_soup)

    def _filename(self):
        filename = self.context.id
        now = datetime.now()
        filename += "_{0}{1}{2}_{3}{4}.pdf".format(
            now.year, now.month, now.day, now.hour, now.minute
        )
        return filename
