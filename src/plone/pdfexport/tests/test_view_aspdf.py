# -*- coding: utf-8 -*-
import unittest

from bs4 import BeautifulSoup
from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.viewlet.interfaces import IViewletManager

from plone import api
from plone.pdfexport.testing import (
    PLONE_PDFEXPORT_FUNCTIONAL_TESTING,
    PLONE_PDFEXPORT_INTEGRATION_TESTING,
)


class ViewsIntegrationTest(unittest.TestCase):

    layer = PLONE_PDFEXPORT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.content.create(self.portal, "Folder", "other-folder")
        api.content.create(self.portal, "News Item", "news-item")

    def test_aspdf_is_registered(self):
        view = getMultiAdapter(
            (self.portal["other-folder"], self.portal.REQUEST), name="aspdf"
        )
        self.assertTrue(view.__name__ == "aspdf")
        view = getMultiAdapter(
            (self.portal["news-item"], self.portal.REQUEST), name="aspdf"
        )
        self.assertTrue(view.__name__ == "aspdf")

    def test_leadimage_viewlet_shows_up_for_newsitems(self):
        from plone.app.contenttypes.behaviors.leadimage import ILeadImage
        from plone.app.layout.globals.interfaces import IViewView
        from zope.interface import alsoProvides

        self.assertTrue(ILeadImage.providedBy(self.portal["news-item"]))
        self.request.set("URL", self.portal["news-item"].absolute_url())
        self.request.set("ACTUAL_URL", self.portal["news-item"].absolute_url())
        self.request.form.update({"html": 1})
        view = self.portal["news-item"].restrictedTraverse("@@aspdf")
        alsoProvides(view, IViewView)
        manager = queryMultiAdapter(
            (self.portal["news-item"], self.request, view),
            IViewletManager,
            "plone.abovecontenttitle",
            default=None,
        )
        self.assertTrue(manager)
        manager.update()
        leadimage_viewlet = [
            v for v in manager.viewlets if v.__name__ == "contentleadimage"
        ]
        self.assertEqual(len(leadimage_viewlet), 1)

    def test_clean_html_with_body_class(self):
        view = self.portal["news-item"].restrictedTraverse("@@aspdf")
        clean_hml_str = view._clean_html(
            raw_html="""
<html>
<head></head>
<body class="template-test-view col-content">
<div>Header</div>

<div id="content" >
<h1>PDF content</h1>
<p>Lorem eiusmod quis adipisicing do exercitation consequat eiusmod est sunt consequat. Sunt magna mollit qui dolore eiusmod ullamco. Qui minim aliquip aute veniam culpa pariatur pariatur cupidatat voluptate voluptate excepteur tempor. Et ea consequat ad voluptate ipsum minim occaecat. Dolore consequat officia aliqua est voluptate do sint voluptate fugiat duis in do sint. Aute exercitation commodo nisi duis non.

Velit laborum exercitation anim sit sunt irure officia ea qui nisi consequat. Magna qui qui commodo nulla laborum non. Nulla sunt amet amet eu magna duis magna sit sint. Magna deserunt reprehenderit qui nostrud fugiat dolor sunt. Commodo nisi ut qui duis eu nisi Lorem sunt. Id adipisicing elit sit in officia veniam eiusmod. Commodo dolore amet deserunt et dolore enim ipsum velit aliquip irure nostrud magna magna veniam.

Fugiat voluptate anim nulla eiusmod sit. Eiusmod irure id voluptate labore. Lorem officia pariatur sunt culpa esse aute anim quis ad enim non nisi Lorem. Cillum duis magna in adipisicing eiusmod tempor tempor labore ullamco excepteur ad officia velit. Deserunt aute ex duis sit et cillum. Tempor irure do eu et sint sint incididunt cupidatat adipisicing fugiat incididunt.</p>
</div>

</body>
</html>
        """
        )
        self.assertTrue(clean_hml_str)
        soup = BeautifulSoup(clean_hml_str, "html.parser")
        content = soup.select_one("#content")
        self.assertEqual(
            content.get("class"),
            ["template-test-view", "col-content"],
        )

    def test_clean_html_with_body_class_preserve_content_classes(self):
        view = self.portal["news-item"].restrictedTraverse("@@aspdf")
        clean_hml_str = view._clean_html(
            raw_html="""
<html>
<head></head>
<body class="template-test-view col-content">
<div>Header</div>

<div id="content" class="content-class">
<h1>PDF content</h1>
<p>Lorem eiusmod quis adipisicing do exercitation consequat eiusmod est sunt consequat. Sunt magna mollit qui dolore eiusmod ullamco. Qui minim aliquip aute veniam culpa pariatur pariatur cupidatat voluptate voluptate excepteur tempor. Et ea consequat ad voluptate ipsum minim occaecat. Dolore consequat officia aliqua est voluptate do sint voluptate fugiat duis in do sint. Aute exercitation commodo nisi duis non.

Velit laborum exercitation anim sit sunt irure officia ea qui nisi consequat. Magna qui qui commodo nulla laborum non. Nulla sunt amet amet eu magna duis magna sit sint. Magna deserunt reprehenderit qui nostrud fugiat dolor sunt. Commodo nisi ut qui duis eu nisi Lorem sunt. Id adipisicing elit sit in officia veniam eiusmod. Commodo dolore amet deserunt et dolore enim ipsum velit aliquip irure nostrud magna magna veniam.

Fugiat voluptate anim nulla eiusmod sit. Eiusmod irure id voluptate labore. Lorem officia pariatur sunt culpa esse aute anim quis ad enim non nisi Lorem. Cillum duis magna in adipisicing eiusmod tempor tempor labore ullamco excepteur ad officia velit. Deserunt aute ex duis sit et cillum. Tempor irure do eu et sint sint incididunt cupidatat adipisicing fugiat incididunt.</p>
</div>

</body>
</html>
        """
        )
        self.assertTrue(clean_hml_str)
        soup = BeautifulSoup(clean_hml_str, "html.parser")
        content = soup.select_one("#content")
        self.assertEqual(
            content.get("class"),
            ["template-test-view", "col-content", "content-class"],
        )

    def test_clean_html_no_body_class(self):
        view = self.portal["news-item"].restrictedTraverse("@@aspdf")
        clean_hml_str = view._clean_html(
            raw_html="""
<html>
<head></head>
<body>
<div>Header</div>

<div id="content">
<h1>PDF content</h1>
<p>Lorem eiusmod quis adipisicing do exercitation consequat eiusmod est sunt consequat. Sunt magna mollit qui dolore eiusmod ullamco. Qui minim aliquip aute veniam culpa pariatur pariatur cupidatat voluptate voluptate excepteur tempor. Et ea consequat ad voluptate ipsum minim occaecat. Dolore consequat officia aliqua est voluptate do sint voluptate fugiat duis in do sint. Aute exercitation commodo nisi duis non.

Velit laborum exercitation anim sit sunt irure officia ea qui nisi consequat. Magna qui qui commodo nulla laborum non. Nulla sunt amet amet eu magna duis magna sit sint. Magna deserunt reprehenderit qui nostrud fugiat dolor sunt. Commodo nisi ut qui duis eu nisi Lorem sunt. Id adipisicing elit sit in officia veniam eiusmod. Commodo dolore amet deserunt et dolore enim ipsum velit aliquip irure nostrud magna magna veniam.

Fugiat voluptate anim nulla eiusmod sit. Eiusmod irure id voluptate labore. Lorem officia pariatur sunt culpa esse aute anim quis ad enim non nisi Lorem. Cillum duis magna in adipisicing eiusmod tempor tempor labore ullamco excepteur ad officia velit. Deserunt aute ex duis sit et cillum. Tempor irure do eu et sint sint incididunt cupidatat adipisicing fugiat incididunt.</p>
</div>

</body>
</html>
        """
        )
        self.assertTrue(clean_hml_str)
        soup = BeautifulSoup(clean_hml_str, "html.parser")
        content = soup.select_one("#content")
        self.assertEqual(
            content.get("class", []),
            [],
        )


class ViewsFunctionalTest(unittest.TestCase):

    layer = PLONE_PDFEXPORT_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
