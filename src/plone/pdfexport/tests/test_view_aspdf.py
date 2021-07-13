# -*- coding: utf-8 -*-
import unittest

from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getMultiAdapter
from zope.component.interfaces import ComponentLookupError

from plone import api
from plone.pdfexport.testing import (
    PLONE_PDFEXPORT_FUNCTIONAL_TESTING,
    PLONE_PDFEXPORT_INTEGRATION_TESTING,
)


class ViewsIntegrationTest(unittest.TestCase):

    layer = PLONE_PDFEXPORT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.content.create(self.portal, "Folder", "other-folder")
        api.content.create(self.portal, "Document", "front-page")

    def test_aspdf_is_registered(self):
        view = getMultiAdapter(
            (self.portal["other-folder"], self.portal.REQUEST), name="aspdf"
        )
        self.assertTrue(view.__name__ == "aspdf")
        view = getMultiAdapter(
            (self.portal["front-page"], self.portal.REQUEST), name="aspdf"
        )
        self.assertTrue(view.__name__ == "aspdf")


class ViewsFunctionalTest(unittest.TestCase):

    layer = PLONE_PDFEXPORT_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
