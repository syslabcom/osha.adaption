from zope import component

from Testing import ZopeTestCase as ztc

from Products.Archetypes.Schema.factory import instanceSchemaFactory
from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase import layer

SiteLayer = layer.PloneSite

class OshaAdaptationLayer(SiteLayer):

    @classmethod
    def setUp(cls):
        ptc.setupPloneSite(products=(
            'osha.adaptation',
            ))

        ztc.installProduct('ATVocabularyManager')
        ztc.installProduct('DataGridField')
        ztc.installProduct('LinguaPlone')
        ztc.installProduct('OSHATranslations')
        ztc.installProduct('VocabularyPickerWidget')
        ztc.installProduct('slc.subtyper')
        ztc.installProduct('slc.treecategories')

        import osha.adaptation
        zcml.load_config('configure.zcml', osha.policy)

        component.provideAdapter(instanceSchemaFactory)
        SiteLayer.setUp()


class OSHAPolicyTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """
    layer = OshaAdaptationLayer


class OSHAPolicyFunctionalTestCase(ptc.FunctionalTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """
    layer = OshaAdaptationLayer
    

