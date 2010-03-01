import unittest
from zope import component
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

            field_obs = obj.Schema().getSchemataFields('default')

            fields = [f.__name__ for f in field_obs]
            config_fields = types_dict[type_name].keys()
            self.assertEquals(
                set(config_fields),
                set(fields),
                "%s has the following Default fields: %s but should " \
                "have %s" % \
                (   type_name,
                    set(fields),
                    set(config_fields),
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

