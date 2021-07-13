# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
    applyProfile,
)
from plone.testing import z2

import plone.pdfexport


class PlonePdfexportLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=plone.pdfexport)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "plone.pdfexport:default")


PLONE_PDFEXPORT_FIXTURE = PlonePdfexportLayer()


PLONE_PDFEXPORT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_PDFEXPORT_FIXTURE,),
    name="PlonePdfexportLayer:IntegrationTesting",
)


PLONE_PDFEXPORT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_PDFEXPORT_FIXTURE,),
    name="PlonePdfexportLayer:FunctionalTesting",
)


PLONE_PDFEXPORT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PLONE_PDFEXPORT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="PlonePdfexportLayer:AcceptanceTesting",
)
