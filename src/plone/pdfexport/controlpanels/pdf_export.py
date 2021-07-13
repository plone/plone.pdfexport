# -*- coding: utf-8 -*-
from plone.app.registry.browser.controlpanel import (
    ControlPanelFormWrapper,
    RegistryEditForm,
)
from plone.autoform import directives
from plone.z3cform import layout
from zope.interface import Interface

from plone import schema
from plone.pdfexport import _


class IPdfExportControlPanel(Interface):
    """PdfExportControlPanel schema"""

    # directives.widget("print_css", klass="print-css")
    print_css = schema.Text(
        title=_(
            u"Print CSS",
        ),
        description=_(
            u'CSS to format the PDF export.\n <a href="https://weasyprint.readthedocs.io/en/stable/tutorial.html" target="_blank">WeasyPrint Docs</a>',
        ),
        required=False,
        default=_(
            u"""/* portrait */
@page {
   margin: 1.4cm 1.4cm 2.75cm 1.4cm;
}

/* landscape*/
/*@page {
   margin: 2.75cm 1.4cm 1.4cm 1.4cm;
   size: landscape;
}*/

body {
    height: 100%;
    display: block;
    font-size:12px;
    color:#444444;
    font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
    font-family: "OpenSans-Regular","HelveticaNeue",Helvetica,Arial,sans-serif;
}
table.listing{
    border-collapse: collapse;
    border: 1px solid #edecec;
    padding: 0.4em;
}
table.listing th{
    border: 1px solid #edecec;
    background-color: #edecec;
    padding: 0.8em;

}
table.listing td{
    border: 1px solid #edecec;
    padding: 0.4em;
    text-align: center;
}
table.listing td:nth-child(1){
    text-align: left;
}

.documentActions,
  #viewlet-below-content-title{
  display: none;
}
        """
        ),
    )


class PdfExportControlPanelForm(RegistryEditForm):
    schema = IPdfExportControlPanel
    schema_prefix = "pdfexport"
    label = u"PDF Export Settings"


PdfExportControlPanelView = layout.wrap_form(
    PdfExportControlPanelForm, ControlPanelFormWrapper
)
