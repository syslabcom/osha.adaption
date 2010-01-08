import unittest

from zope import component

from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.extender import set_schema_order

from Products.Archetypes.utils import OrderedDict
from Products.CMFCore.utils import getToolByName

from p4a.subtyper.interfaces import ISubtyper

from base import OshaAdaptationTestCase

from osha.adaptation.config import EXTENDED_TYPES_DEFAULT_FIELDS

types_dict = EXTENDED_TYPES_DEFAULT_FIELDS.copy()

class TestSchemaExtender(OshaAdaptationTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()

    def test_schema_modifications(self):
        """ Test that the extended types have the right fields in the correct
            order.
        """
        for type_name in types_dict:
            order = None
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

            extenders = list(component.getAdapters((obj,), ISchemaExtender))
            modifiers = list(component.getAdapters((obj,), ISchemaModifier))

            for name, extender in extenders:
                if IOrderableSchemaExtender.providedBy(extender):
                    order = extender.getOrder(original)

            if order is not None:
                set_schema_order(schema, order)

            if len(modifiers) > 0:
                for name, modifier in modifiers:
                    modifier.fiddle(schema)

            field_obs = schema.getSchemataFields('default')
            fields = [f.__name__ for f in field_obs]
            config_fields = types_dict[type_name].keys()
            self.assertEquals(
                config_fields,
                fields,
                "%s has the following Default fields: %s but should " \
                "have %s" % \
                (   type_name, 
                    fields,
                    config_fields, 
                )
            )
            
            for i in range(0, len(fields)):
                self.assertEquals(
                    field_obs[i].widget.visible,
                    types_dict[type_name][fields[i]],
                    "%s has field %s with widget visibility: %s but it should " \
                    "be %s" % \
                    (   type_name, 
                        fields[i],
                        field_obs[i].widget.visible,
                        types_dict[type_name][fields[i]], 
                    )
                )


    def is_subtyped(self, obj):
        subtyper = component.getUtility(ISubtyper)
        type = subtyper.existing_type(obj)
        if type:
            return type.name == 'annotatedlinks'
        else:
            return False


    def test_subtyping(self):
        self.portal.invokeFactory('Document', 'Document')
        obj = self.portal._getOb('Document')

        subtyper = component.getUtility(ISubtyper)
        subtyper.change_type(obj, 'annotatedlinks')

        self.assertEquals(self.is_subtyped(obj), True)

        subtyper = component.getUtility(ISubtyper)
        subtyper.remove_type(obj)

        self.assertEquals(self.is_subtyped(obj), False)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSchemaExtender))
    return suite

