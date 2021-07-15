# -*- coding: utf-8 -*-
import unittest

from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.component.interfaces import ComponentLookupError
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


class ViewsFunctionalTest(unittest.TestCase):

    layer = PLONE_PDFEXPORT_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
