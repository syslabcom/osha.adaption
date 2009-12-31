import unittest

from zope.component import getAdapters

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.extender import set_schema_order

from Products.Archetypes.utils import OrderedDict
from Products.CMFCore.utils import getToolByName

from base import OshaAdaptationTestCase

from osha.adaptation.config import EXTENDED_TYPES_DEFAULT_FIELDS

types_dict = EXTENDED_TYPES_DEFAULT_FIELDS.copy()

class TestSchemaExtender(OshaAdaptationTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()

    def test_default_fields(self):
        """ Test the extended schema of a document
        """
        for type_name in types_dict:
            pt = getToolByName(self.portal, 'portal_types')
            info = pt.getTypeInfo(type_name)
            obj = info.constructInstance(self.portal, type_name)
            schema = obj.Schema()

            # Get the correct ordering of the fields by calling the modifiers
            # and extenders registered for the object, as is done in 
            # archetypes.schemaextender/schemaextender/extender.py
            original = OrderedDict()
            for name in schema.getSchemataNames():
                schemata_fields = schema.getSchemataFields(name)
                original[name] = list(x.getName() for x in schemata_fields)

            extenders = list(getAdapters((obj,), ISchemaExtender))
            modifiers = list(getAdapters((obj,), ISchemaModifier))
            for name, extender in extenders:
                if IOrderableSchemaExtender.providedBy(extender):
                    order = extender.getOrder(original)

            if order is not None:
                set_schema_order(schema, order)


            if len(modifiers) > 0:
                for name, modifier in modifiers:
                    modifier.fiddle(schema)

            fields = [f.__name__ for f in schema.getSchemataFields('default')]
            self.assertEquals(
                types_dict[type_name],
                fields,
                    "%s has the following Default fields: %s but should " \
                    "have %s" % \
                    (   type_name, 
                        fields,
                        types_dict[type_name]
                    )
                )

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSchemaExtender))
    return suite

