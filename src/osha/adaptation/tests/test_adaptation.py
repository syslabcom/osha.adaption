import unittest

from zope.component import getAdapters

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender

from Products.Archetypes.utils import OrderedDict
from Products.CMFCore.utils import getToolByName

from base import OshaAdaptationTestCase

from osha.adaptation.config import EXTENDED_TYPES_DEFAULT_FIELDS

types_dict = EXTENDED_TYPES_DEFAULT_FIELDS.copy()


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

class TestSchemaExtender(OshaAdaptationTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()

    def populate_site(self):
        """ Populate the test instance with content.
        """
        for type in types_dict.keys():
            # Create an object for each portal_type which is extended
            # The id is the same as the type
            pt = getToolByName(self.portal, 'portal_types')
            self.portal.invokeFactory(type, type)

    def test_default_fields(self):
        """
        Test the extended schema of a document
        """
        self.populate_site()

        for type in types_dict:
            obj = self.portal.get(type)

            schema = obj.Schema()
            default_schema = schema.getSchemataFields("default")
            fields = [i.__name__ for i in default_schema]

            sorted_returned_fields = list(fields)
            sorted_returned_fields.sort()

            sorted_default_fields = list(types_dict[type])
            sorted_default_fields.sort()

            self.assertEquals(
                sorted_default_fields,
                sorted_returned_fields,
                "The sorted fields of %s: %s do not match the sorted default "
                "fields: %s" \
                % (type, sorted_returned_fields, sorted_default_fields))

            original = OrderedDict()
            for name in schema.getSchemataNames():
                schemata_fields = schema.getSchemataFields(name)
                original[name] = list(x.getName() for x in schemata_fields)

            extenders = list(getAdapters((obj,), ISchemaExtender))
            for name, extender in extenders:
                if IOrderableSchemaExtender.providedBy(extender):
                    ordered_returned_fields = extender.getOrder(original)

            self.assertEquals(
                types_dict[type],
                ordered_returned_fields['default'],
                    "%s has the following Default fields: %s but should " \
                    "have %s" % \
                    (   type, 
                        ordered_returned_fields['default'], 
                        types_dict[type]
                    )
                )

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSchemaExtender))
    return suite

