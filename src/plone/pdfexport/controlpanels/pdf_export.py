# -*- coding: utf-8 -*-
from plone import schema
from plone.app.registry.browser.controlpanel import (
    ControlPanelFormWrapper,
    RegistryEditForm,
)
from plone.z3cform import layout
from plone.pdfexport import _
from plone.formwidget.namedfile.widget import NamedImageFieldWidget
from zope.interface import Interface


class IPdfExportControlPanel(Interface):
    """PdfExportControlPanel schema"""

    default_mode = schema.Choice(
        title=_(
            u'Default mode',
        ),
        description=_(
            u'Choose if Portrait or Landscape mode should be the default.\nYou can override it later with ?mode=landscape url parameter.',
        ),
        vocabulary="plone.pdfexport.AvailablePageModes",
        default=u"portrait",
        # defaultFactory=get_default_default_mode,
        required=False,
        readonly=False,
    )

    print_image_scale = schema.Choice(
        title=_(
            u"Print Image Scale",
        ),
        description=_(
            u"Image scale to use for PDF Export.",
        ),
        vocabulary=u"plone.app.vocabularies.ImagesScales",
        default=u"large",
        # defaultFactory=get_default_print_scale,
        required=True,
    )

    banner = schema.Bytes(
        title=_(
            u'Banner / Logo image',
        ),
        description=_(
            u'An image to show above the first page.',
        ),
        required=False,
        readonly=False,
    )

    portrait_css = schema.SourceText(
        title=_(
            u'Portrait page definitions',
        ),
        description=_(
            u'Define page setting for the portrait mode',
        ),
        default=u"""/* portrait */
@page {
   margin: 1.4cm 1.4cm 2.75cm 1.4cm;
   @top-center {
     font-size:12px;
     color:#666666;
     content: "Beautiful Plone content, deserves a beautiful PDF export!";
   }
   @bottom-left {
     font-size:12px;
     color:#666666;
     content: "provided by derico.de";
   }
   @bottom-right {
     font-size:12px;
     color:#666666;
     content: "Page " counter(page);
   }
}
        """,
        required=False,
        readonly=False,
    )

    landscape_css = schema.SourceText(
        title=_(
            u'Landscape page definitions',
        ),
        description=_(
            u'Define page setting for the landscape mode',
        ),
        default=u"""/* landscape*/
@page {
   margin: 1.5cm 1.5cm 1.5cm 1.5cm;
   size: landscape;
   @top-center {
     font-size:12px;
     color:#666666;
     content: "Beautiful Plone content, deserves a beautiful PDF export!";
   }
   @bottom-left {
     font-size:12px;
     color:#666666;
     content: "provided by derico.de";
   }
   @bottom-right {
     font-size:12px;
     color:#666666;
     content: "Page " counter(page);
   }
}
        """,
        required=False,
        readonly=False,
    )

    # directives.widget("print_css", klass="print-css")
    print_css = schema.Text(
        title=_(
            u"Print CSS",
        ),
        description=_(
            u'CSS to format the PDF export.\n <a href="https://weasyprint.readthedocs.io/en/stable/tutorial.html" target="_blank">WeasyPrint Docs</a>',
        ),
        required=False,
        default=u"""/*
.newsImageContainer{
  text-align: center;
}*/

.newsImageContainer img{
  max-width: 80%;
  max-height: 80%;
}

img{
  max-width: 80%;
  max-height: 80%;
}
body {
    height: 100%;
    display: block;
    font-size:12px;
    color:#444444;
    font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
    font-family: "OpenSans-Regular","HelveticaNeue",Helvetica,Arial,sans-serif;
}
table.listing,
table{
    border-collapse: collapse;
    border: 1px solid #edecec;
    padding: 0.4em;
}
table.listing th{
    border: 1px solid #edecec;
    background-color: #edecec;
    padding: 0.8em;

}
table.listing td,
table td{
    border: 1px solid #edecec;
    padding: 0.4em;
    text-align: center;
}
table.listing td:nth-child(1){
    text-align: left;
}

.documentActions,
.documentByLine{
  display: none;
}

/* some useful Plone default styles */
.image-right {
    float: right;
    margin: .5em;
}
.image-left {
    float: left;
    margin: .5em 1em .5em 0;
}
.documentDescription {
    font-size: 16px;
    font-weight: 700;
    color: #696969;
    margin-bottom: 10px;
}
.newsImageContainer {
    float: right;
    margin: 0 0 6px 6px;
}
        """,
    )


class PdfExportControlPanelForm(RegistryEditForm):
    schema = IPdfExportControlPanel
    schema_prefix = "pdfexport"
    label = u"PDF Export Settings"

    def updateFields(self):
        super(PdfExportControlPanelForm, self).updateFields()
        self.fields['banner'].widgetFactory = NamedImageFieldWidget


PdfExportControlPanelView = layout.wrap_form(
    PdfExportControlPanelForm, ControlPanelFormWrapper
)
