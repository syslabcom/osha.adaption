import unittest

from zope.component import getAdapters

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender

from Products.Archetypes.utils import OrderedDict

from base import OshaAdaptationTestCase

from osha.adaptation.config import DEFAULT_FIELDS


#    'Blob', no content type
#    'RichDocument', ua
#    'NewsItem', no content type

# (Pdb) self.portal.invokeFactory("SPSpeaker", "asdf")
# *** ValueError: No such content type: SPSpeaker
# (Pdb) self.portal.invokeFactory("SPSpeechVenue", "asdf")
# *** ValueError: No such content type: SPSpeechVenue
#slc.seminarportal
# (Pdb) self.portal.invokeFactory("HelpCenterFAQ", "asdf")
# *** ValueError: No such content type: HelpCenterFAQ
#PloneHelpCenter

EXTENDED_TYPES = [
    'Link',
    'Image',
    'File',
    'Document',
    'Event',
    'PressRelease',
    'CaseStudy',
    'RALink',
    ]

class TestSchemaExtender(OshaAdaptationTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()

    def populate_site(self):
        """ Populate the test instance with content.
        """
        for type in EXTENDED_TYPES:
            # Create an object for each portal_type which is extended
            # The name is the same as the type
            self.portal.invokeFactory(type, type)

    def test_default_fields(self):
        """
        Test the extended schema of a document
        """
        self.populate_site()

        for type in EXTENDED_TYPES:
            obj = self.portal.get(type)

            schema = obj.Schema()
            default_schema = schema.getSchemataFields("default")
            fields = [i.__name__ for i in default_schema]

            sorted_returned_fields = fields
            sorted_returned_fields.sort()

            sorted_default_fields = DEFAULT_FIELDS[type]
            sorted_default_fields.sort()

            self.assertEquals(
                sorted_default_fields,
                sorted_returned_fields,
                "The sorted fields of %s: %s do not match the sorted default "
                "fields: %s" \
                % (type, sorted_returned_fields, sorted_default_fields))
        
            original = OrderedDict()
            for name in schema.getSchemataNames():
                fields = schema.getSchemataFields(name)
                original[name] = list(x.getName() for x in fields)

            extenders = list(getAdapters((obj,), ISchemaExtender))
            for name, extender in extenders:
                if IOrderableSchemaExtender.providedBy(extender):
                    ordered_returned_fields = extender.getOrder(original)

            self.assertEquals(
                DEFAULT_FIELDS[type],
                ordered_returned_fields,
                "%s has the following Default fields: %s but should have %s"
                %(type, fields, DEFAULT_FIELDS[type]))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSchemaExtender))
    return suite

