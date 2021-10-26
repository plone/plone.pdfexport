# -*- coding: utf-8 -*-
import unittest

from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory, IVocabularyTokenized

from plone.pdfexport import _
from plone.pdfexport.testing import PLONE_PDFEXPORT_INTEGRATION_TESTING  # noqa


class AvailablePageModesIntegrationTest(unittest.TestCase):

    layer = PLONE_PDFEXPORT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_vocab_available_page_modes(self):
        vocab_name = "plone.pdfexport.AvailablePageModes"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))
        self.assertEqual(
            vocabulary.getTerm("sony-a7r-iii").title,
            _(u"Sony Aplha 7R III"),
        )
