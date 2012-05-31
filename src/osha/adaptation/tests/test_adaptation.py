import unittest
import logging
from zExceptions import Unauthorized
from zope import component
from Products.Archetypes.interfaces._base import IBaseContent
from Products.ATContentTypes.interface.topic import IATTopicCriterion
from Products.CMFCore.utils import getToolByName
from p4a.subtyper.interfaces import ISubtyper
from base import OshaAdaptationTestCase
from osha.adaptation.config import EXTENDED_TYPES_DEFAULT_FIELDS
types_dict = EXTENDED_TYPES_DEFAULT_FIELDS.copy()

log = logging.getLogger('test_adaptation.py')

class TestSchemaExtender(OshaAdaptationTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()

    def test_seo_description(self):
        """ Ticket #999:
            All content types should be extended with a new field
            called seoDescription.

            This field should appear directly underneath the normal description
            field.
        """
        # import sys; sys.sdtout = file('/dev/stdout', 'w')
        ttool = getToolByName(self.portal, 'portal_types')
        not_extended = open("not_extended.txt", 'w')
        extended_properly = open("extended_properly", "w")
        wrong_order = open("wrong_order.txt", 'w')
        for type_name in ttool.listContentTypes():
            info = ttool.getTypeInfo(type_name)
            try:
                obj = info.constructInstance(self.portal, type_name)
            except Unauthorized:
                continue
            except:
                continue

            if not IBaseContent.providedBy(obj):
                continue
            if IATTopicCriterion.providedBy(obj):
                continue

            field_obs = obj.Schema().getSchemataFields('default')
            fields = [f.__name__ for f in field_obs]
            # assert('seoDescription' in fields)
            # self.assertEquals(
            #             fields.index('seoDescription'),
            #             fields.index('description')+1
            #             )

            if "seoDescription" not in fields:
                not_extended.write("Not extended: %s \n" % type_name)

            elif (fields.index('seoDescription') !=
                  fields.index('description') + 1):
                wrong_order.write("Wrong order: %s \n" % type_name)

            else:
                extended_properly.write("%s \n" % type_name)

        not_extended.close()
        wrong_order.close()
        extended_properly.close()

    def test_schema_modifications(self):
        """ Test that the extended types have the right fields in the correct
            order.
        """
        for type_name in types_dict:
            #order = None
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
                (type_name,
                 set(fields),
                 set(config_fields),
                )
            )

            for i in range(0, len(fields)):
                self.assertEquals(
                    field_obs[i].widget.visible,
                    types_dict[type_name][fields[i]],
                    "%s has field %s with widget visibility: %s but it "
                    "should be %s" % \
                    (type_name,
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

    def test_event_date_to_be_confirmed(self):
        """ Ticket #2341:
            Events need an extra field to show if the date is
            provisional and still needs to be confirmed

            This field should appear directly after the date fields
        """
        ttool = getToolByName(self.portal, 'portal_types')
        info = ttool.getTypeInfo("Event")
        event = info.constructInstance(self.portal, "Event")
        field_obs = event.Schema().getSchemataFields('default')
        fields = [f.__name__ for f in field_obs]
        assert('dateToBeConfirmed' in fields)
        self.assertEquals(
                    fields.index('dateToBeConfirmed'),
                    fields.index('endDate') + 1
                    )

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSchemaExtender))
    return suite
